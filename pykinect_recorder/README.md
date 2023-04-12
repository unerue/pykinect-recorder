# Coding convention

## Comment (주석)

Comment is capitalize.
```python
# We have a pineapple
def get_a_apple(): pass
```

```python
# Wrong
class IMUViewer: pass
# Correct
class ImuViewer: pass

```

## Module organization

pykinect_recorder
- main
- renderer
    - custom_widgets.py
    - components
        - viewer_audio.py
        - viewer_audio.stylesheet


e.g.: viewer_audio.ts -> viewer_audio.module.css

```python
class CustomWidget(QFrame):
    pass


class DlViewer: pass
class DeepLearningViewer: pass

class DeeLearningViewer(QFrame):
    def __init__(self):
        layout = QHBoxLayout(self)
        main_layout = QHBoxLayout()
        main_widget = QWidget()
        sub_layout = QVBoxLayout()
        subsub_layout = QHBoxLayout()


        layout_main = QHBoxLayout()
        widget_main = QWidget()
        
        frame_name = QFrame()
        layout_sub = QVBoxLayout()


        button_start = QPushButton()
        btn_start = QPushButton()
        combo_rgb_control = QComboBox()
        combo_rgb_control.addItems([])
        cb_rgb_control.addItems([])
        cb_rgb_ctl.
        # attribute is a noun
        # method front verb setItems, addWidgets
        self.set
```