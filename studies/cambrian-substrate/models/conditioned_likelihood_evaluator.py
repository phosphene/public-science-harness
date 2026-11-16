"""
Canonical Conditioned Birth-Death Likelihood Evaluator.
Implements PSH-BD-003 and DEC-PYRATE-001/003: Evaluates exact joint log-likelihoods
conditioned on Keiding ascertainment, composing pure mathematical primitives.
Ref: Kendall (1948), Bartlett (1949), Keiding (1975), Silvestro et al. (2014, 2019).
"""

from __future__ import annotations

import hashlib
import math
from typing import Dict, Sequence, Tuple
import numpy as np
from pydantic import Field

from phosphene.harness.data.core.vitals import InvariantStatic
from birth_death_primitives import (
    keiding_sampling_probability,
    poisson_occurrence_loglik,
    lineage_survival_loglik,
    diversity_dependent_hazard,
)
from lineage_horizon_evaluator import StratigraphicEvaluationReceipt, LineageObservationEnvelope


class BirthDeathParameters(InvariantStatic):
    """
    Continuous-time rates governing speciation, extinction, and fossil preservation.
    """
    lambda_0: float = Field(..., ge=0.0, description="Baseline continuous-time speciation rate (events / Myr / lineage)")
    mu_0: float = Field(..., ge=0.0, description="Baseline continuous-time extinction rate (events / Myr / lineage)")
    q_0: float = Field(..., ge=0.0, description="Poisson preservation / sampling rate (finds / Myr / lineage)")
    gl: float = Field(default=0.0, description="Speciation diversity-dependence feedback slope")
    gm: float = Field(default=0.0, description="Extinction diversity-dependence feedback slope")


class TaxonLikelihoodBreakdown(InvariantStatic):
    """
    Component-level log-likelihood evaluation for a single lineage.
    """
    taxon_name: str
    s_origination_ma: float
    e_extinction_ma: float
    duration_myr: float
    occurrence_count: int
    loglik_occurrences: float
    loglik_survival: float
    log_keiding_conditioning: float
    total_conditioned_loglik: float


class BirthDeathLikelihoodReceipt(InvariantStatic):
    """
    Cryptographically sealed likelihood receipt for an entire cohort of taxa.
    """
    total_log_likelihood: float
    loglik_occurrences_total: float
    loglik_survival_total: float
    log_keiding_conditioning_total: float
    n_taxa: int
    parameters: BirthDeathParameters
    taxon_breakdowns: dict[str, TaxonLikelihoodBreakdown]
    sha256_digest: str


class ConditionedBirthDeathLikelihoodEvaluator:
    """
    Evaluates exact continuous-time Markov birth-death-sampling likelihoods
    conditioned on Keiding observation probability P(K > 0 | s, e, q).
    """

    @staticmethod
    def evaluate_cohort_likelihood(
        cohort_receipt: StratigraphicEvaluationReceipt,
        latent_spans: dict[str, tuple[float, float]],
        parameters: BirthDeathParameters,
        standing_diversity: float = 0.0,
    ) -> BirthDeathLikelihoodReceipt:
        """
        Evaluates the joint log-likelihood across all taxa in the receipt.
        
        Args:
            cohort_receipt: The evaluated stratigraphic FAD/LAD cohort receipt.
            latent_spans: Dict of taxon_name -> (s_i, e_i) candidate true lifespan bounds.
            parameters: Macroevolutionary parameters (lambda_0, mu_0, q_0, gl, gm).
            standing_diversity: Current active lineage count N_t for diversity-dependence.
        """
        if parameters.q_0 <= 0.0:
            raise ValueError("Preservation rate q_0 must be strictly positive.")

        # Compute effective diversity-dependent rates
        lam_eff = float(diversity_dependent_hazard(standing_diversity, parameters.lambda_0, parameters.gl, model="linear"))
        mu_eff = float(diversity_dependent_hazard(standing_diversity, parameters.mu_0, parameters.gm, model="linear"))
        q = parameters.q_0

        breakdowns: dict[str, TaxonLikelihoodBreakdown] = {}
        total_occ_ll = 0.0
        total_surv_ll = 0.0
        total_keid_ll = 0.0

        for taxon_name, env in sorted(cohort_receipt.taxon_envelopes.items()):
            if taxon_name not in latent_spans:
                raise KeyError(f"Latent span (s, e) missing for taxon {taxon_name}")

            s_i, e_i = latent_spans[taxon_name]

            # Invariant 1: Structural stratigraphic boundaries
            # s_i >= FAD >= LAD >= e_i >= 0.0
            if s_i < env.fad_ma or e_i > env.lad_ma or e_i < 0.0:
                # Boundary violation: returns negative infinity
                total_ll = -float("inf")
                sha = hashlib.sha256(f"INVALID:{taxon_name}:{s_i}:{e_i}".encode("utf-8")).hexdigest()
                return BirthDeathLikelihoodReceipt(
                    total_log_likelihood=-float("inf"),
                    loglik_occurrences_total=-float("inf"),
                    loglik_survival_total=-float("inf"),
                    log_keiding_conditioning_total=0.0,
                    n_taxa=len(cohort_receipt.taxon_envelopes),
                    parameters=parameters,
                    taxon_breakdowns={},
                    sha256_digest=sha,
                )

            duration = round(s_i - e_i, 4)
            k = env.total_occurrences

            # Term 1: Poisson occurrence log-likelihood
            # log L_occ = k * log(q) - q * (s - e)
            occ_ll = k * math.log(q) - (q * duration)

            # Term 2: Continuous-time survival log-likelihood (Keiding / Kendall)
            # log L_surv = - (lam + mu) * (s - e) + log(mu) (assuming extinct in fossil record)
            is_extant = (e_i == 0.0)
            surv_ll = lineage_survival_loglik(s_i, e_i, lam_eff, mu_eff, is_extant=is_extant)

            # Term 3: Keiding conditioning normalizer
            # P(K > 0 | s, e, q) = 1 - exp(-q * (s - e))
            p_obs = keiding_sampling_probability(s_i, e_i, q)
            if p_obs <= 0.0:
                keid_ll = -float("inf")
            else:
                keid_ll = math.log(p_obs)

            # Conditioned log-likelihood for taxon i:
            # log L_i = log L_occ + log L_surv - log P(K > 0)
            taxon_total_ll = occ_ll + surv_ll - keid_ll

            breakdown = TaxonLikelihoodBreakdown(
                taxon_name=taxon_name,
                s_origination_ma=round(s_i, 4),
                e_extinction_ma=round(e_i, 4),
                duration_myr=duration,
                occurrence_count=k,
                loglik_occurrences=round(occ_ll, 6),
                loglik_survival=round(surv_ll, 6),
                log_keiding_conditioning=round(keid_ll, 6),
                total_conditioned_loglik=round(taxon_total_ll, 6),
            )
            breakdowns[taxon_name] = breakdown

            total_occ_ll += occ_ll
            total_surv_ll += surv_ll
            total_keid_ll += keid_ll

        total_conditioned_loglik = total_occ_ll + total_surv_ll - total_keid_ll

        # Compute deterministic provenance hash
        hash_input = f"{total_conditioned_loglik:.6f}:{parameters.model_dump_json()}:{len(breakdowns)}"
        sha = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

        return BirthDeathLikelihoodReceipt(
            total_log_likelihood=round(total_conditioned_loglik, 6),
            loglik_occurrences_total=round(total_occ_ll, 6),
            loglik_survival_total=round(total_surv_ll, 6),
            log_keiding_conditioning_total=round(total_keid_ll, 6),
            n_taxa=len(breakdowns),
            parameters=parameters,
            taxon_breakdowns=breakdowns,
            sha256_digest=sha,
        )
