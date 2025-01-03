import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QCursor

class MultiSelectComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.selected_items = []
        
        # Configure view
        view = QListView()
        view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setView(view)
        
        # Setup combo box
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        
        # Connect signals
        self.view().clicked.connect(self.on_item_clicked)
        
    def on_item_clicked(self, index):
        item = self.model().data(index, Qt.DisplayRole)
        if item in self.selected_items:
            self.selected_items.remove(item)
        else:
            self.selected_items.append(item)
            
        # Update selection in view
        self.view().selectionModel().select(
            index, 
            QItemSelectionModel.Select if item in self.selected_items 
            else QItemSelectionModel.Deselect
        )
        
        # Update display text
        self.setEditText(' | '.join(self.selected_items))
        self.showPopup()
        print("Selected items:", self.selected_items)
        
    def hidePopup(self):
        if not self.view().rect().contains(self.view().mapFromGlobal(QCursor.pos())):
            super().hidePopup()

    def get_selected_items(self):
        return self.selected_items


class BoardGameGenerator(QMainWindow):
    def update_selected_types(self, index):
        selected_items = self.type_combo.view().selectionModel().selectedIndexes()
        selected_types = [self.type_combo.itemText(i.row()) for i in selected_items]
        print("Selected game types:", selected_types)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('桌游推荐器')
        self.setFixedSize(800, 900)

        # 数据定义
        self.game_types = ['abstract_strategy', 'adventure', 'age_of_reason', 'american_west', 'ancient', 'animals', 'card_game', 'city_building', 'civilization', 'deduction', 'dice', 'economic', 'environmental', 'exploration', 'fantasy', 'farming', 'fighting', 'humor', 'industry_/_manufacturing', 'medical', 'medieval', 'miniatures', 'modern_warfare', 'mythology', 'nautical', 'negotiation', 'novel-based', 'number', 'party_game', 'political', 'post-napoleonic', 'puzzle', 'religious', 'renaissance', 'science_fiction', 'space_exploration', 'spies_/_secret_agents', 'territory_building', 'trains', 'transportation', 'travel', 'wargame', 'word_game']
        self.durations = ["不限", "30分钟以内", "30-60分钟", "1-2小时", "2小时以上"]
        self.styles = ["不限", "轻度策略", "中度策略", "重度策略", "休闲", "竞技"]

        # 主界面设置
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 游戏类型选择
        layout.addWidget(QLabel("游戏类型:"))
        self.type_combo = MultiSelectComboBox()
        self.type_combo.addItems(self.game_types)
        self.type_combo.setEditable(True)
        self.type_combo.setInsertPolicy(QComboBox.NoInsert)
        self.type_combo.setMaxVisibleItems(len(self.game_types))
        layout.addWidget(self.type_combo)

        # 游戏时长选择
        layout.addWidget(QLabel("游戏时长:"))
        self.duration_combo = QComboBox()
        self.duration_combo.addItems(self.durations)
        layout.addWidget(self.duration_combo)

        # 游戏风格选择
        layout.addWidget(QLabel("游戏风格:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems(self.styles)
        layout.addWidget(self.style_combo)

        # 玩家人数选择
        layout.addWidget(QLabel("玩家人数:"))
        self.player_spin = QSpinBox()
        self.player_spin.setRange(1, 8)
        self.player_spin.setValue(4)
        layout.addWidget(self.player_spin)

        # 生成按钮
        self.generate_button = QPushButton("推荐桌游")
        self.generate_button.clicked.connect(self.generate_game)
        layout.addWidget(self.generate_button)

        # 结果显示
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                background-image: url('path/to/your/background.jpg');
                background-repeat: no-repeat;
                background-position: center;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 14px;
                margin: 5px 0;
            }
            QComboBox {
                padding: 5px;
                margin: 5px 0;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QSpinBox {
                padding: 5px;
                margin: 5px 0;
            }
        """)

    def generate_game(self):
        game_type = self.type_combo.currentText()
        duration = self.duration_combo.currentText()
        style = self.style_combo.currentText()
        players = self.player_spin.value()

        result = f"""
筛选条件:
游戏类型: {game_type}
游戏风格: {style}
游戏时长: {duration}
玩家人数: {players} 人

建议:
根据您的选择，可以考虑以下类型的游戏...
        """
        self.result_label.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BoardGameGenerator()
    window.show()
    sys.exit(app.exec_())