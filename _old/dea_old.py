# # ==========================================
# # DEA module.
# # Date: 2020/04/21
# # Latest: 2021/02/09
# # Author: Takeshi Morinibu.
# # ==========================================

# # Import library.
# # import warnings
# import numpy as np
# import pulp


# class DEA:
#     def __init__(self, orient="in", model="envelope"):
#         """[summary]

#         Args:
#             orient (str, optional): [in or out]. Defaults to "in".
#             model (str, optional): [envelope or multiple]. Defaults to "envelope".
#         """
#         self.orient = self._set_input(orient, ["in", "out"])
#         self.model = self._set_input(model, ["envelope", "multiple"])
#         self.method = None
#         self.inputs = None
#         self.outputs = None
#         self.result = None
#         self._N = 0  # Number of the DMUs
#         self._m = 0  # Dimension of the inputs
#         self._s = 0  # Dimension of the outputs
#         self.sign_figs = 8

#     def _set_input(self, value, valid_list):
#         if value in valid_list:
#             return value
#         else:
#             _sent = " or ".join(valid_list)
#             raise ValueError(f"input must be {_sent}.")

#     def fit(self, inputs, outputs, method="CRS", uncontrollable_index=None):
#         """[summary]

#         Args:
#             inputs (np.array): [description]
#             outputs (np.array): [description]
#             method (str, optional): [CRS, VRS]. Defaults to "CRS".
#         """
#         self.method = self._set_input(method, ["CRS", "VRS"])
#         self.inputs = inputs
#         self.outputs = outputs
#         self._set_dimension()
#         self.u_c_index = self._set_u_c_index(uncontrollable_index)

#         self.result = self._process_lp()

#     # Initialize objective function.
#     def _init_problem(self):
#         # Envelope (in => min, out => max)
#         if self.model == "envelope":
#             if self.orient == "in":
#                 problem = pulp.LpProblem(self.orient, pulp.LpMinimize)
#             else:
#                 problem = pulp.LpProblem(self.orient, pulp.LpMaximize)
#         # Multiple (in => max, out => min)
#         else:
#             if self.orient == "in":
#                 problem = pulp.LpProblem(self.orient, pulp.LpMaximize)
#             else:
#                 problem = pulp.LpProblem(self.orient, pulp.LpMinimize)
#         return problem

#     def _set_dimension(self):
#         self._N = self.inputs.shape[0]
#         self._m = self.inputs.shape[1]
#         self._s = self.outputs.shape[1]

#     def _set_u_c_index(self, index):
#         if self.orient == "in":
#             index_max = self._m
#         else:
#             index_max = self._s

#         if index is None:
#             pass
#         elif index < index_max:
#             pass
#         else:
#             raise ValueError("The index out of range.")
#         return index

#     def _dict_to_list(self, _dict):
#         return [_dict[k] for k in _dict]

#     def _rounder(self, v):
#         return round(v, self.sign_figs)

#     def _process_lp(self):
#         if self.model == "envelope":
#             res = [self._envelope_model(j) for j in range(self._N)]
#         else:
#             res = [self._multiple_model(j) for j in range(self._N)]
#         return res

#     # Envelope model.
#     def _envelope_model(self, o):
#         # Define problem and variables.
#         problem = self._init_problem()
#         lambda_N = self._dict_to_list(
#             pulp.LpVariable.dicts(
#                 "Lambda", range(self._N), lowBound=0, cat="Continuous"
#             )
#         )
#         theta = pulp.LpVariable("theta", lowBound=0)

#         # Define objective.
#         problem += theta

#         if self.orient == "in":
#             in_coef = theta
#             out_coef = 1
#         else:
#             in_coef = 1
#             out_coef = theta

#         # Add restrictions.
#         for i in range(self._m):
#             # Process uncontrollable variables.
#             if i == self.u_c_index:
#                 in_coef = 1
#             else:
#                 in_coef = theta
#             problem += (
#                 pulp.lpDot(lambda_N, self.inputs[:, i]) <= in_coef * self.inputs[o, i]
#             )
#         for i in range(self._s):
#             problem += (
#                 pulp.lpDot(lambda_N, self.outputs[:, i])
#                 >= out_coef * self.outputs[o, i]
#             )

#         if self.method == "VRS":
#             problem += np.sum(lambda_N) == 1

#         # Solve and add results.
#         problem.solve()

#         eff = self._rounder(problem.objective.value())
#         lambda_list = [self._rounder(n.value()) for n in lambda_N]
#         output = {"eff": eff, "lambda": lambda_list}

#         return self._verify_output(o, output)

#     # Multiple model.
#     def _multiple_model(self, o):
#         # Define problem and variables.
#         problem = self._init_problem()
#         mu = self._dict_to_list(pulp.LpVariable.dicts("Mu", range(self._s), lowBound=0))
#         nu = self._dict_to_list(pulp.LpVariable.dicts("Nu", range(self._m), lowBound=0))

#         # Define objective.
#         if self.method == "VRS":
#             bias = pulp.LpVariable("bias", lowBound=0)
#         else:
#             bias = 0

#         # Add restrictions.
#         if self.orient == "in":
#             problem += pulp.lpDot(mu, self.outputs[o, :]) + bias

#             for j in range(self._N):
#                 problem += (
#                     pulp.lpDot(mu, self.outputs[j, :])
#                     - pulp.lpDot(nu, self.inputs[j, :])
#                     + bias
#                     <= 0
#                 )

#             problem += pulp.lpDot(nu, self.inputs[o, :]) == 1
#         else:
#             problem += pulp.lpDot(nu, self.inputs[o, :]) + bias

#             for j in range(self._N):
#                 problem += (
#                     pulp.lpDot(nu, self.inputs[j, :])
#                     - pulp.lpDot(mu, self.outputs[j, :])
#                     + bias
#                     >= 0
#                 )

#             problem += pulp.lpDot(mu, self.outputs[o, :]) == 1

#         # Solve and add results.
#         problem.solve(pulp.PULP_CBC_CMD(msg=1, gapRel=1e-10, options=["revised"]))

#         eff = self._rounder(problem.objective.value())

#         weight_x = [i.value() for i in nu]
#         weight_y = [r.value() for r in mu]

#         output = {"eff": eff, "weight": {"x": weight_x, "y": weight_y}}

#         if self.method == "VRS":
#             output.update({"bias": bias.value()})

#         return self._verify_output(o, output)

#     # Its only for slack.
#     def _slack_optimization(self, o, theta):
#         # Define problem and variables.
#         sx = self._dict_to_list(pulp.LpVariable.dicts("sx", range(self._m), lowBound=0))
#         sy = self._dict_to_list(pulp.LpVariable.dicts("sy", range(self._s), lowBound=0))
#         lambda_N = self._dict_to_list(
#             pulp.LpVariable.dicts("Lambda", range(self._N), lowBound=0)
#         )

#         problem = pulp.LpProblem("slack", pulp.LpMaximize)
#         problem += np.sum(sx) + np.sum(sy)

#         # Add restrictions.
#         if self.orient == "in":
#             in_coef = theta
#             out_coef = 1
#         else:
#             in_coef = 1
#             out_coef = theta

#         for i in range(self._m):
#             problem += (
#                 pulp.lpDot(lambda_N, self.inputs[:, i]) + sx[i]
#                 == in_coef * self.inputs[o, i]
#             )

#         for r in range(self._s):
#             problem += (
#                 pulp.lpDot(lambda_N, self.outputs[:, r]) - sy[r]
#                 == out_coef * self.outputs[o, r]
#             )
#         problem += np.sum(lambda_N) == 1

#         # Solve and add results.
#         problem.solve(pulp.PULP_CBC_CMD(msg=1, gapRel=1e-10, options=["revised"]))

#         return {"sx": [i.value() for i in sx], "sy": [r.value() for r in sy]}

#     # Verify the slack.
#     def _add_slack_result(self, r, output):
#         output.update(r)
#         if np.sum(r["sx"]) + np.sum(r["sy"]) > 0:
#             output.update(dict(slack=True))
#         else:
#             output.update(dict(slack=False))

#     def _verify_output(self, o, output):
#         if output["eff"] == 1:
#             r = self._slack_optimization(o, output["eff"])
#             self._add_slack_result(r, output)
#         else:
#             pass
#         return output
