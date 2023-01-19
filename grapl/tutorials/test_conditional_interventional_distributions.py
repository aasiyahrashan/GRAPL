import grapl.algorithms as algs
import grapl.dsl as dsl
import grapl.expr as expr
import grapl.util as util
import dsep

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
    X; Z; Y; \
    Z -> Y; \
    X <-> Z; '

G = grapl_obj.readgrapl(dag_grapl)
G.display()

num, num_expr, isident_num = algs.idfixing(G, {'X'}, {'Y', 'Z'})
denom, denom_expr, isident_denom = algs.idfixing(G, {'X'}, {'Z'})

output = str(num) +  '/' + str(denom)

output = expr.Expr(num=num_expr, den=denom_expr)
# output.simplify()
string_output = output.tostr()



markov_string, markov_true = algs.localmarkov(G)
print(markov_string, markov_true)

# Function to redefine string.

def swap_strings(X, Y, Z):
    newdict = {'X': X, 'Y': Y, 'Z': Z}

    output = list()
    for key, value in newdict.items():
        output.extend(key)

    newstring = str(output[1]) + '⊥' + str(output[2]) + '| ' + str(output[0])
    return newstring


### Function for step 1

def conditional_intervention_distribution(Y, X, Z, G):

    ## Step 1.

    ## Creating a new version of the graph where all nodes up from x and down from z are deleted.
    G = G.delete_incoming('X')
    G = G.delete_outgoing('Z')

    # testing if y is conditionally independent of Z locally.
    # Assuming there's only one Z.
    #if len(Z) > 1:

    if dsep.dsep(Y, Z, X, G) == 'd-separated':
        #conditional_intervention_distribution(Y, Z, X, G)
        pass
     # Step 2. If not true, using the ID function.
    else:
        num, num_expr, isident_num = algs.idfixing(G, X, {Y, Z})
        denom, denom_expr, isident_denom = algs.idfixing(G, X, {Z})

    output = str(num) +  '/' + str(denom)
    return output

    #
    #
    # for x in markov_string:
    #     if swap_strings(X, Y, Z) in x:
    #         print('Yes')
    #     else:
    #         print(swap_strings(X, Y, Z))
    #         # condition_1 = True

    # If this is ever true, return the recursion with another z

    # return output

G_edited = conditional_intervention_distribution('Y', 'X', 'Z', G)
G_edited.display()
G_edited.pa('X')
G_edited.ch('Z')

print('done')