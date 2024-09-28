import graphviz

class FlowchartGenerator:
    def __init__(self):
        self.graph = graphviz.Digraph(comment='Flowchart')
        self.graph.node('Start', 'Start', shape='oval')
        self.current_node = 'Start'
        self.nodes_created = set()  

    def add_node(self, name, label, shape):
        if name not in self.nodes_created: 
            self.graph.node(name, label, shape=shape)
            self.nodes_created.add(name)

    def generate_flowchart(self, c_code):
        lines = c_code.strip().split('\n')
        in_if_block = False

        for line in lines:
            line = line.strip()

            if line.startswith('void ') or line.startswith('int '):
                func_name = line.split(' ')[1].split('(')[0]
                self.add_node(func_name, func_name, 'rectangle')
                self.graph.edge(self.current_node, func_name)
                self.current_node = func_name

            elif 'scanf' in line:  # Handle input
                self.add_node('Input_A', 'Input A', 'parallelogram')  # Block for Input A
                self.graph.edge(self.current_node, 'Input_A')
                self.current_node = 'Input_A'
                
                self.add_node('Input_B', 'Input B', 'parallelogram')  # Block for Input B
                self.graph.edge(self.current_node, 'Input_B')
                self.current_node = 'Input_B'

            elif line.startswith('if '):
                condition = line.split('if ')[1].split('{')[0].strip()
                self.add_node(condition, f'if ({condition})', 'diamond')
                self.graph.edge(self.current_node, condition)

                self.current_node = condition  
                in_if_block = True  

            elif 'printf' in line:
                print_stmt = line.split('printf')[1].split(';')[0].strip()
                self.add_node(print_stmt, f'Output: {print_stmt}', 'parallelogram')
                self.graph.edge(self.current_node, print_stmt)

                if in_if_block:  
                    in_if_block = False  

            elif line.startswith('else'):
                self.current_node = condition
                continue  

            elif line == '}':
                if not in_if_block:
                    self.current_node = 'Start'  

        self.graph.render('flowchart', format='png')
        print("Flowchart generated and saved as 'flowchart.png'.")

# Example C code to generate flowchart
c_code = """
#include <stdio.h>

void main() {
   scanf("%d%d", &a, &b);  // Input for A and B

   int c = a + b;

   if (c > a && c > b) {
       printf("C greater");
   }
   else {
        printf("C not greater");
   }
}
"""

# Running the flowchart generator
generator = FlowchartGenerator()
generator.generate_flowchart(c_code)
