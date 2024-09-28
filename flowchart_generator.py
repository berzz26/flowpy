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

            elif '=' in line:
                var_name, value = line.split('=')
                var_name = var_name.strip()
                value = value.split(';')[0].strip()  
                self.add_node(var_name, f'{var_name} = {value}', 'rectangle') 
                self.graph.edge(self.current_node, var_name)

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

# put your C code to generate flowchart
#sample code
c_code = """  /
#include <stdio.h>

void main() {
   int a = 10;
   int b = 20;

   int c = a + b;

   if (c > 15) {
       printf("%d", c);
   }
   else {
        printf("Nono");
   }
}
"""

generator = FlowchartGenerator()
generator.generate_flowchart(c_code)
