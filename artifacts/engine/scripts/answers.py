import subprocess, hashlib, sys
V = sys.argv[1]
P = "PREFIX ex: <http://example.org/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX dbo: <http://dbpedia.org/ontology/> "
Q = {
 "vf_tri_rows": "SELECT ?a ?b ?c WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?a dbo:location ?c }",
 "vf_tri_cyc_rows": "SELECT ?a ?b ?c WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?c dbo:location ?a }",
 "vf_tri_count": "SELECT (COUNT(*) AS ?n) WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?a dbo:location ?c }",
 "vf_tri_cyc_count": "SELECT (COUNT(*) AS ?n) WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?c dbo:location ?a }",
 "vf_tri_sel": "SELECT ?a ?b ?c WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?a ex:rare ?c }",
 "vf_cycle_quad": "SELECT ?a ?b WHERE { ?a foaf:knows ?x . ?b ex:related ?x . ?b dbo:location ?z . ?a dbo:birthPlace ?z }",
 "vf_nt_chain": "SELECT ?b ?c ?d WHERE { ex:n100 foaf:knows ?b . ?b ex:related ?c . ?c dbo:location ?d }",
 "vf_nt_star": "SELECT (COUNT(*) AS ?n) WHERE { ?a ex:rare ?b . ?a foaf:knows ?c . ?b ex:related ?d }",
 "x_tri_limit": "SELECT ?a ?b ?c WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?a dbo:location ?c } ORDER BY ?a ?b ?c LIMIT 5",
 "x_tri_distinct_a": "SELECT (COUNT(DISTINCT ?a) AS ?n) WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?c dbo:location ?a }",
}
bad = 0
for ds in ["skew.lb", "skew.ttl", "uni.lb", "medium.lb", "medium.ttl"]:
    for k, q in Q.items():
        h = {}
        for b in "AN":
            r = subprocess.run([f"{V}/{b}/zig-out/bin/leatherback", "query", P + q, f"{V}/data/{ds}"], capture_output=True)
            lines = sorted(r.stdout.decode().splitlines())
            h[b] = (r.returncode, len(lines), hashlib.sha256("\n".join(lines).encode()).hexdigest()[:12])
        same = h["A"] == h["N"] and h["A"][0] == 0
        bad += not same
        print(f"{ds},{k},A={h['A']},N={h['N']},{'SAME' if same else 'DIFF'}", flush=True)
print("DIFFS", bad)
