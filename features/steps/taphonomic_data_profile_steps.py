import sqlite3
from pathlib import Path
from behave import given, when, then


@given("an audited Cambrian occurrence database with {count:d} total occurrences")
def step_open_db(context, count):
    context.db_path = Path(__file__).parent.parent.parent / "studies/cambrian-substrate/data/curated/cambrian_substrate.db"
    assert context.db_path.exists()
    conn = sqlite3.connect(context.db_path)
    c = conn.cursor()
    c.execute("SELECT count(*) FROM cambrian_occurrences;")
    total = c.fetchone()[0]
    conn.close()
    assert total == count, f"Expected {count} occurrences, got {total}"


@when("the occurrence frequency per taxon is profiled")
def step_profile_frequency(context):
    conn = sqlite3.connect(context.db_path)
    c = conn.cursor()
    c.execute("SELECT count(DISTINCT taxon_name) FROM cambrian_occurrences;")
    context.distinct_taxa = c.fetchone()[0]
    
    c.execute("""
        SELECT count(*) FROM (
            SELECT taxon_name FROM cambrian_occurrences GROUP BY taxon_name HAVING count(*) = 1
        );
    """)
    context.singletons = c.fetchone()[0]
    conn.close()


@then("exactly {count:d} distinct taxa must be identified")
def step_assert_taxa_count(context, count):
    assert context.distinct_taxa == count, f"Expected {count} taxa, got {context.distinct_taxa}"


@then("exactly {count:d} taxa must appear as singletons with occurrence count 1")
def step_assert_singletons(context, count):
    assert context.singletons == count, f"Expected {count} singletons, got {context.singletons}"


@then("the singleton proportion must exceed {pct:d} percent of all taxa")
def step_assert_singleton_pct(context, pct):
    ratio = (context.singletons / context.distinct_taxa) * 100.0
    assert ratio > pct, f"Singleton pct {ratio:.2f}% did not exceed {pct}%"


@when("the spatial clustering across collections is evaluated")
def step_eval_clustering(context):
    conn = sqlite3.connect(context.db_path)
    c = conn.cursor()
    c.execute("SELECT count(DISTINCT pbdb_collection_no) FROM cambrian_occurrences;")
    context.n_collections = c.fetchone()[0]
    
    c.execute("""
        SELECT pbdb_collection_no, count(DISTINCT taxon_name)
        FROM cambrian_occurrences
        GROUP BY pbdb_collection_no
        HAVING count(DISTINCT taxon_name) >= 20;
    """)
    context.dense_collections = c.fetchall()
    conn.close()


@then("the occurrences must be distributed across exactly {count:d} distinct collections")
def step_assert_collections_count(context, count):
    assert context.n_collections == count, f"Expected {count} collections, got {context.n_collections}"


@then("at least {count:d} collections must represent dense Lagerstatte beds with 20 or more taxa")
def step_assert_dense_count(context, count):
    assert len(context.dense_collections) >= count, f"Expected >= {count} dense collections, got {len(context.dense_collections)}"


@when("occurrences are partitioned by functional ecological guild")
def step_partition_guilds(context):
    conn = sqlite3.connect(context.db_path)
    c = conn.cursor()
    c.execute("""
        SELECT functional_guild, count(*), count(DISTINCT taxon_name)
        FROM cambrian_occurrences
        GROUP BY functional_guild;
    """)
    context.guild_data = {row[0]: (row[1], row[2]) for row in c.fetchall()}
    conn.close()


@then("the infaunal burrower guild must contain exactly {occs:d} body occurrences across {taxa:d} taxa")
def step_assert_infaunal_body(context, occs, taxa):
    actual_occs, actual_taxa = context.guild_data["INFAUNAL_BURROWER"]
    assert actual_occs == occs, f"Expected {occs} infaunal occurrences, got {actual_occs}"
    assert actual_taxa == taxa, f"Expected {taxa} infaunal taxa, got {actual_taxa}"


@then("mobile predators with cuticular hardware must contain over {count:d} occurrences")
def step_assert_pred_count(context, count):
    actual_occs, actual_taxa = context.guild_data["MOBILE_APEX_PREDATOR"]
    assert actual_occs > count, f"Expected > {count} predator occurrences, got {actual_occs}"


@then("the taphonomic body disparity ratio between predators and infauna must exceed {ratio:d} to 1")
def step_assert_disparity(context, ratio):
    pred_occs = context.guild_data["MOBILE_APEX_PREDATOR"][0]
    inf_occs = context.guild_data["INFAUNAL_BURROWER"][0]
    actual_ratio = pred_occs / inf_occs
    assert actual_ratio > ratio, f"Expected disparity > {ratio}, got {actual_ratio:.2f}"
