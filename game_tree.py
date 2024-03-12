import copy


class Node:
    def __init__(self, id, number, human_score, ai_score, bank, level):
        self.id = id
        self.number = number
        self.human_score = human_score
        self.ai_score = ai_score
        self.bank = bank
        self.level = level

class Game_tree:
    def __init__(self, number):
        self.prime_node = Node(1, number, 0, 0, 0, 1)
        self.set_of_prime_nodes = []
        self.set_of_nodes = []
        self.dictionary = dict()
        self.coeffs = [2, 3, 4]

        self.generate_prime_tree()

    def generate_prime_tree(self):
        self.create_tree(self.prime_node)
        self.set_of_prime_nodes = copy.deepcopy(self.set_of_nodes)
        self.set_of_nodes.clear()

    def adding_node(self, Node):
        self.set_of_nodes.append(Node)

    def adding_node_to_layer(self, initial_node_id, end_node_id):
        self.dictionary[initial_node_id] = self.dictionary.get(initial_node_id, []) + [end_node_id]

    def create_tree(self, initial_node):
        self.set_of_nodes.append(initial_node)
        j = initial_node.id + 1
        upper_layer = [initial_node]
        lower_layer = []
        human_score = initial_node.human_score
        ai_score = initial_node.ai_score
        bank_score = initial_node.bank
        while len(upper_layer) > 0:
            for i in upper_layer:
                if i.number <= 5000:
                    numbers = [i.number * self.coeffs[0], i.number * self.coeffs[1], i.number * self.coeffs[2]]
                    tmp_three_numbers = []
                    for k in numbers:
                        if (i.level + 1) % 2 == 0:
                            ai_score = i.ai_score
                            if k % 2 == 0:
                                human_score = i.human_score - 1
                            else:
                                human_score = i.human_score + 1

                            if k % 5 == 0:
                                bank_score = i.bank + 1

                            if k >= 5000:
                                human_score += bank_score
                        else:
                            human_score = i.human_score

                            if k % 2 == 0:
                                ai_score = i.ai_score - 1
                            else:
                                ai_score = i.ai_score + 1

                            if k % 5 == 0:
                                bank_score = i.bank + 1

                            if k >= 5000:
                                ai_score += bank_score
                        node = Node(j, k, human_score, ai_score, bank_score, i.level + 1)
                        lower_layer.append(node)
                        self.set_of_nodes.append(node)
                        tmp_three_numbers.append(node)
                        self.adding_node_to_layer(i.id, node.id)
                        j += 1
            upper_layer = copy.deepcopy(lower_layer)
            lower_layer.clear()

    def find_node(self, number, level):
        for i in self.set_of_prime_nodes:
            if number == i.number and level == i.level:
                return i

        return None

    def move_checking(self, number, level):
        current_node = self.find_node(number, level)
        tmp_num = number
        level_of_fastest_win = current_node.level
        weights = [0,0,0]
        for j in self.coeffs:
            self.create_tree(self.find_node(number*j, level + 1))
            while tmp_num < 5000:
                tmp_num *= 4
                level_of_fastest_win += 1

            for k in self.set_of_nodes:
                if k.level >= level_of_fastest_win:
                    if k.number >= 5000:
                        if k.level % 2 != 0:
                            if k.ai_score > k.human_score + k.bank:
                                weights[j - 2] += 1
                            elif k.ai_score < k.human_score + k.bank:
                                weights[j - 2] -= 1
                        else:
                            if k.ai_score + k.bank > k.human_score:
                                weights[j - 2] += 1
                            elif k.ai_score + k.bank < k.human_score:
                                weights[j - 2] -= 1

        return self.coeffs[weights.index(max(weights))]



# def print_tree(node, prefix=''):
#     # Вывод текущего узла
#     print(f"{prefix}{node.id}: {node.number}")
#     # Если у узла есть дочерние элементы, рекурсивно выводим их
#     if node.id in gt.dictionary:
#         for child_id in gt.dictionary[node.id]:
#             # Находим дочерний узел по его ID
#             child_node = next((n for n in gt.set_of_nodes if n.id == child_id), None)
#             if child_node:
#                 # Вызываем функцию рекурсивно для дочернего узла
#                 # Добавляем к префиксу символы для сдвига вправо
#                 print_tree(child_node, prefix + '    ')
#
# gt = Game_tree(35)
# print(gt.move_checking(35, 1))

# if gt.set_of_nodes:
#     print_tree(gt.set_of_nodes[0])
#
# for x in gt.set_of_nodes:
#     print(x.id, x.number, x.human_score, x.ai_score, x.bank,x.level)
#
# print(len(gt.set_of_nodes))
# for x, y in gt.dictionary.items():
#     print(x, y)

#gt.adding_node(Node('A1', 36, 0, 0, 0, 1))
# nodes_generated.append(['A1', 36, 0, 0, 0, 1])
#
# while len(nodes_generated) > 0:
#     current_node = nodes_generated[0]
#     move_checking(2, nodes_generated, current_node)
#
#     move_checking(3, nodes_generated, current_node)
#
#     move_checking(4, nodes_generated, current_node)
#     nodes_generated.pop(0)