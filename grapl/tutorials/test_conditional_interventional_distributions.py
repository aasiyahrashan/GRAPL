import grapl.algorithms as algs
import grapl.dsl as dsl
import grapl.expr as expr
import grapl.util as util
import dsep
import copy as cp
#
# # Creating an example graph.
# grapl_obj = dsl.GraplDSL()
#
# # Create a DAG from a GRAPL string
# dag_grapl = ' "conditional interventional distribution"; \
#     X; Z; Y; \
#     X -> Z; \
#     Y -> Z; \
#     X <-> Z; '
# G = grapl_obj.readgrapl(dag_grapl)
# G.display()
#
#
# #####
#
# id_str, expr, isident = algs.idfixing(G, {'X'}, {'Y'})
# if isident:
#     print(id_str) # p_{X}(Y)=\sum_{M,X'}[p(Y|M,X')p(M|X)p(X')]
# else:
#     print('Interventional distribution not identifiable')
#
# markov_string, markov_true = algs.localmarkov(G)
# print(markov_string)

### Trying independences for G''
grapl_obj = dsl.GraplDSL()
# dag_grapl = ' "conditional interventional distribution complicated"; \
#     X; Z; Y; W; A; B; \
#     B -> X; \
#     X -> Z; \
#     Y -> Z; \
#     W -> Y; \
#     Z -> A; \
#     X <-> Z; '

# dag_grapl = ' "conditional interventional distribution complicated"; \
#     X; Z; Y; W; \
#     W -> X; \
#     W -> Z; \
#     X -> Z; \
#     Z -> Y; \
#     X <-> Y; '

# dag_grapl = ' "conditional interventional distribution complicated"; \
#     X; Z; Y; W; \
#     W -> Y; \
#     Z -> Y; \
#     Y -> X; \
#     Z -> X; '

# dag_grapl = ' "conditional interventional distribution complicated"; \
#     V; X; Y; Z; W; \
#     V -> X; \
#     X -> Y; \
#     X -> Z; \
#     Z -> W; '

dag_grapl = ' "conditional interventional distribution complicated"; \
    X; Z; Y; A; \
    Z -> Y; \
    A -> Y; \
    X <-> Z; '

G = grapl_obj.readgrapl(dag_grapl)
G.display()

num, num_expr, isident_num = algs.idfixing(G, {'X'}, {'Y', 'Z'})
denom, denom_expr, isident_denom = algs.idfixing(G, {'X'}, {'Z'})

output = str(num) +  '/' + str(denom)

def conditional_intervention_distribution(Y, X, Z, G):

    ## Step 1.

    ## Creating a new version of the graph where all nodes up from x and down from z are deleted.
    G_original = cp.deepcopy(G)
    G.delete_incoming(X)
    G.delete_outgoing(Z)

    # testing if y is conditionally independent of Z locally.
    # Assuming there's only one Z.
    if len(Z) > 1:
        for z in Z:
            if dsep.dsep(Y, z, X, G) == 'd-separated':
                # This needs to call the function again, but with the z we used addded to X and removed from Z.
                X.add(z)
                Z.remove(z)
                conditional_intervention_distribution(Y, X, Z, G_original)
     # Step 2. If not true, using the ID function.
    else:
        joint_y_z_set = Y.union(Z)
        num, num_expr, isident_num = algs.idfixing(G_original, X, joint_y_z_set)
        denom, denom_expr, isident_denom = algs.idfixing(G_original, X, Z)

    output = str(num) +  '/' + str(denom)
    return output

identifiable = conditional_intervention_distribution({'Y'}, {'X'}, {'Z'}, G)


print('done')