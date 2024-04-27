import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QRadioButton
import analysis as AN
import functions as FN
import matplotlib as mtl
import numpy as np

class GUI(QWidget):

    def __init__(self):

        super().__init__()
        self.setWindowTitle('Truss Analysis')


        self.radioValueFD = None
        self.radioValueXY = None

        self.boundaryValues = []
        self.nodeList = []
        self.elementList = []
        

        # Container for Values
        self.material_property = (None, None)

        # Set up the layout
        layout = QGridLayout()
        
        layout.addWidget(self.materialPropertyLayout(), 0, 0, 1, 1)
        layout.addWidget(self.boundaryConditionLayout(), 1, 0, 1, 1)
        layout.addWidget(self.insertNodes(), 2, 0, 1, 1)
        

        # Create QTextBrowser widget
        self.text_browser = QTextBrowser()

        #self.setCentralWidget(self.text_browser)
        layout.addWidget(self.text_browser, 0, 1, 3, 1)
        # You can set initial text here
        self.text_browser.setText(AN.df)

        self.run_program()

        self.setLayout(layout)

    def materialPropertyLayout(self):
        
        # Create input widgets
        youngs_modulus_input = QLineEdit()
        cross_sectional_area_input = QLineEdit()

        youngs_modulus_input.setFixedWidth(80)
        cross_sectional_area_input.setFixedWidth(80)

        # Create submit button
        submit_button = QPushButton('Submit')

        mat_layout = QGroupBox("Material Property")
        layout = QGridLayout()
        
        layout.addWidget(QLabel("Young's Modulus: "), 0, 0)
        layout.addWidget(youngs_modulus_input, 0, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(QLabel("Area of Cross-Section: "), 1, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(cross_sectional_area_input, 1, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(submit_button, 2, 0)
        result_label = QLabel('Result')
        layout.addWidget(result_label)

        mat_layout.setLayout(layout)

        submit_button.clicked.connect(lambda: self.get_yAndE(youngs_modulus_input.text(),
                                                                  cross_sectional_area_input.text(), result_label))

        return mat_layout

    def boundaryConditionLayout(self):

        node_number_input = QLineEdit()
        magnitude_input = QLineEdit()

        node_number_input.setFixedWidth(80)
        magnitude_input.setFixedWidth(80)

        apply_button = QPushButton("Submit")
        cancel_button = QPushButton("Cancel")

        # Radio buttons for direction (X, Y)
        dir_group_box = QGroupBox("Direction")
        dir_layout = QVBoxLayout()
        rb_X = QRadioButton("X")
        rb_Y = QRadioButton("Y")
        dir_layout.addWidget(rb_X)
        dir_layout.addWidget(rb_Y)
        dir_group_box.setLayout(dir_layout)

        # Radio buttons for boundary conditions (Force, Displacement)
        bc_group_box = QGroupBox("Boundary Condition")
        bc_layout = QVBoxLayout()
        rb_Force = QRadioButton("force")
        rb_Displace = QRadioButton("displacement")
        bc_layout.addWidget(rb_Force)
        bc_layout.addWidget(rb_Displace)
        bc_group_box.setLayout(bc_layout)

        bc_layout = QGroupBox("Boundary Condition")
        layout = QGridLayout()
        
        layout.addWidget(QLabel("Node Number"), 0, 0)
        layout.addWidget(dir_group_box, 0, 1)
        layout.addWidget(bc_group_box, 0, 2)
        layout.addWidget(QLabel("Magnitude"), 0, 3)
        layout.addWidget(apply_button, 0, 4)

        
        layout.addWidget(node_number_input, 1, 0)
        layout.addWidget(magnitude_input, 1, 3)
        layout.addWidget(cancel_button, 1, 4)


        bc_layout.setLayout(layout)

        # Connect radio button signals to handler functions
        dir_group = QButtonGroup(self)
        dir_group.addButton(rb_X)
        dir_group.addButton(rb_Y)
        dir_group.buttonClicked.connect(self.onClickedXY)

        bc_group = QButtonGroup(self)
        bc_group.addButton(rb_Force)
        bc_group.addButton(rb_Displace)
        bc_group.buttonClicked.connect(self.onClickedFD)

        result_label = QLabel('Result')
        layout.addWidget(result_label, 3, 1)

        apply_button.clicked.connect(lambda: self.get_boundary(node_number_input.text(),
                                                               self.radioValueXY,
                                                               self.radioValueFD,
                                                               magnitude_input.text()))

    
        return bc_layout
        
    def insertNodes(self):
        
        # Create input widgets
        nodes = QLabel("Nodes")
        ni_x = QLineEdit()
        ni_y = QLineEdit()


        elements = QLabel("Elements")
        end_node_1 = QLineEdit()
        end_node_2 = QLineEdit()

        ni_x.setFixedWidth(80)
        ni_y.setFixedWidth(80)

        end_node_1.setFixedWidth(80)
        end_node_2.setFixedWidth(80)

        # Create submit button
        node_button = QPushButton("Generate Node")
        element_button = QPushButton("Element Node")

        mat_layout = QGroupBox("Nodal Section")
        layout = QGridLayout()
        
        layout.addWidget(nodes, 0, 2)
        layout.addWidget(QLabel("X"), 1, 0)
        layout.addWidget(ni_x, 2, 0, Qt.AlignmentFlag.AlignLeft)
        
        layout.addWidget(QLabel("Y"), 1, 3)
        layout.addWidget(ni_y, 2, 3, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(node_button, 3, 2, Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(elements, 4, 2)
        layout.addWidget(QLabel("End Node 1"), 5, 0)
        layout.addWidget(end_node_1, 6, 0, Qt.AlignmentFlag.AlignLeft)
        
        layout.addWidget(QLabel("End Node 2"), 5, 3)
        layout.addWidget(end_node_2, 6, 3, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(element_button, 7, 2, Qt.AlignmentFlag.AlignCenter)

    
        run_button = QPushButton("Run")
        layout.addWidget(run_button , 8, 2, Qt.AlignmentFlag.AlignCenter)

        node_button.clicked.connect(lambda: self.get_node(ni_x.text(),
                                                                  ni_y.text()))
        
        element_button.clicked.connect(lambda: self.get_element(end_node_1.text(),
                                                                  end_node_2.text()))
        
        run_button.clicked.connect(self.run_program)

        mat_layout.setLayout(layout)


        return mat_layout
    
    def onClickedFD(self,btn):
        self.radioValueFD = btn.text()


    def onClickedXY(self, btn):
        self.radioValueXY = btn.text()


    def get_yAndE(self, E, A, C):
        try:
            Young = float(E)
            Area = float(A)
            self.material_Property = (Young, Area)
            C.setText(f"{self.material_Property}")
        except ValueError:
            self.ERROR()


    def get_boundary(self, node, cordn, state, mag):
        try:
            N = int(node)
            axis = cordn
            force_or_displacement = state
            value = -1 if mag == "0" else float(mag)
            self.boundaryValues.append([node, axis, force_or_displacement, value])
        except ValueError:
            self.ERROR()

    def get_node(self, n1, n2):
        try:
            first = n1
            second = n2
            if (first, second) not in self.nodeList:
                self.nodeList.append((first, second))
            else:
                self.ERROR("Node already exists")
            
        except ValueError:
            self.ERROR("Insert a numeral")

    def get_element(self, e1, e2):
        try:
            first = e1
            second = e2
            if (first, second) not in self.elementList:
                self.elementList.append((first, second))
            else:
                self.ERROR("Element already exists")
        except ValueError:
            self.ERROR("Insert a numeral")
        
    def ERROR(self, message):
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setText("Error")
            self.msg.setInformativeText(message)
            self.msg.setWindowTitle("Error")
            self.msg.exec_()
            return None
    

    def run_program(self):

        AN.NL = np.array(self.nodeList)
        AN.EL = np.array(self.elementList)
        AN.Fu = np.array(self.process_data_Force(self.boundaryValues))
        AN.U_u = np.array(self.process_data_Displacement(self.boundaryValues))
        AN.DorN = np.array(self.process_data_DorN(self.boundaryValues))

        AN.E = self.material_property[0]
        AN.A = self.material_property[1]

        
        print("Force: ", AN.Fu)
        print("Displacement: ", AN.U_u)

        return 0


    def process_data_Force(self, data):
        new_array = []
        for i in range(len(data)):
            if data[i][2] == 'force':
                node = data[i][0]
                axis_values = []
                for j in range(len(data)):
                    if data[j][0] == node and data[j][2] == 'force':
                        axis_values.append(data[j][3])
                if len(axis_values) == 2:
                    new_array.append(axis_values)

        result = new_array.copy()
        # Convert to tuples before applying set for hashing
        value = set(map(tuple, result))
        new_List = []
        for each in value:
            new_List.append(list(each))

        new_List = np.array(new_List)
        return np.array(new_List)
    
    def process_data_Displacement(self, data):
        new_array = []
        for i in range(len(data)):
            if data[i][2] == 'displacement':
                node = data[i][0]
                axis_values = []
                for j in range(len(data)):
                    if data[j][0] == node and data[j][2] == 'displacement':
                        axis_values.append(data[j][3])
                if len(axis_values) == 2:
                    new_array.append(axis_values)

        result = new_array.copy()
        # Convert to tuples before applying set for hashing
        value = set(map(tuple, result))
        new_List = []
        for each in value:
            new_List.append(list(each))

        new_List = np.array(new_List)
        return np.array(new_List)
    
    def process_data_DorN(self, data):
        new_array = []
        processed_nodes = set()  # Keep track of processed nodes
        for i in range(len(data)):
            if data[i][2] in ['F', 'D'] and data[i][0] not in processed_nodes:
                node = data[i][0]
            axis_values = []
            for j in range(len(data)):
                if data[j][0] == node and data[j][2] in ['F', 'D']:
                    axis_values.append(1 if data[j][3] != 0 else -1)
            if len(axis_values) == 2:
                new_array.append(axis_values)
            processed_nodes.add(node)  # Mark node as processed
        return np.array(new_array)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())

