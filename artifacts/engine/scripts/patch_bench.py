import sys
p = sys.argv[1]
s = open(p).read()
anchor = "pub const query_bench_suite = [_]QueryBenchCase{\n"
assert s.count(anchor) == 1
cases = r'''    // verifier cases (scratch build only).
    .{ .id = "vf_tri_rows", .sparql = query_prefixes ++
        \\SELECT ?a ?b ?c WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?a dbo:location ?c }
    },
    .{ .id = "vf_tri_cyc_rows", .sparql = query_prefixes ++
        \\SELECT ?a ?b ?c WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?c dbo:location ?a }
    },
    .{ .id = "vf_tri_count", .sparql = query_prefixes ++
        \\SELECT (COUNT(*) AS ?n) WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?a dbo:location ?c }
    },
    .{ .id = "vf_tri_cyc_count", .sparql = query_prefixes ++
        \\SELECT (COUNT(*) AS ?n) WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?c dbo:location ?a }
    },
    .{ .id = "vf_tri_sel", .sparql = query_prefixes ++
        \\SELECT ?a ?b ?c WHERE { ?a foaf:knows ?b . ?b ex:related ?c . ?a ex:rare ?c }
    },
    .{ .id = "vf_cycle_quad", .sparql = query_prefixes ++
        \\SELECT ?a ?b WHERE { ?a foaf:knows ?x . ?b ex:related ?x . ?b dbo:location ?z . ?a dbo:birthPlace ?z }
    },
    .{ .id = "vf_nt_chain", .sparql = query_prefixes ++
        \\SELECT ?b ?c ?d WHERE { ex:n100 foaf:knows ?b . ?b ex:related ?c . ?c dbo:location ?d }
    },
    .{ .id = "vf_nt_star", .sparql = query_prefixes ++
        \\SELECT (COUNT(*) AS ?n) WHERE { ?a ex:rare ?b . ?a foaf:knows ?c . ?b ex:related ?d }
    },
'''
s = s.replace(anchor, anchor + cases)
old = "            if (exec_ns < best_exec_ns) best_exec_ns = exec_ns;\n"
assert s.count(old) == 2
s = s.replace(old, old + '            std.debug.print("VFTIME,{s},{d},{d}\\n", .{ case.id, exec_ns, row_count });\n')
open(p, "w").write(s)
print("patched", p)
