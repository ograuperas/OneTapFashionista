import 'package:flex_color_picker/flex_color_picker.dart';
import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:sm_flutter/icons/my_flutter_app_icons.dart';

class ColorPickerPage extends StatefulWidget {
  static const routeName = '/colorPicker';

  @override
  _ColorPickerPageState createState() => _ColorPickerPageState();
}

class _ColorPickerPageState extends State<ColorPickerPage> {
  // Color for the picker in a dialog using onChanged.
  Color dialogPickerColor;

  @override
  void initState() {
    super.initState();
    dialogPickerColor = Colors.red; // Material red.
  }

  Future<bool> colorPickerDialog() async {
    return ColorPicker(
      // Use the dialogPickerColor as start color.
      color: dialogPickerColor,
      // Update the dialogPickerColor using the callback.
      onColorChanged: (Color color) =>
          setState(() => dialogPickerColor = color),
      width: 40,
      height: 40,
      borderRadius: 4,
      spacing: 5,
      runSpacing: 5,
      wheelDiameter: 155,
      heading: Text(
        'Select color',
        style: Theme.of(context).textTheme.subtitle1,
      ),
      subheading: Text(
        'Select color shade',
        style: Theme.of(context).textTheme.subtitle1,
      ),
      wheelSubheading: Text(
        'Selected color and its shades',
        style: Theme.of(context).textTheme.subtitle1,
      ),
      showColorName: true,
      copyPasteBehavior: const ColorPickerCopyPasteBehavior(
        longPressMenu: true,
      ),
      materialNameTextStyle: Theme.of(context).textTheme.caption,
      colorNameTextStyle: Theme.of(context).textTheme.caption,
      colorCodeTextStyle: Theme.of(context).textTheme.caption,
      pickersEnabled: const <ColorPickerType, bool>{
        ColorPickerType.primary: true,
        ColorPickerType.accent: true,
        ColorPickerType.wheel: true,
      },
    ).showPickerDialog(
      context,
      constraints:
          const BoxConstraints(minHeight: 460, minWidth: 300, maxWidth: 320),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('wowowow'),
        toolbarHeight: 70,
        actions: <Widget>[
          Padding(
            padding: EdgeInsets.only(right: 20.0),
            child: InkWell(
              onTap: () {
                // TODO save image to gallery
              },
              child: Icon(
                Icons.save,
                size: 50,
              ),
            ),
          ),
        ],
      ),
      body: Container(
        color: Colors.white,
        child: ColorIndicator(
          width: 44,
          height: 44,
          borderRadius: 4,
          color: dialogPickerColor,
          onSelectFocus: false,
          onSelect: () async {
            // Store current color before we open the dialog.
            final Color colorBeforeDialog = dialogPickerColor;
            // Wait for the picker to close, if dialog was dismissed,
            // then restore the color we had before it was opened.
            if (!(await colorPickerDialog())) {
              setState(() {
                dialogPickerColor = colorBeforeDialog;
              });
            }
          },
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: HexColor('#75CD9B'),
        items: <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(MyFlutterApp.trousers),
            label: 'Trousers',
          ),
          BottomNavigationBarItem(
            icon: Icon(MyFlutterApp.tshirt),
            label: 'T-shirt',
          ),
          BottomNavigationBarItem(
            icon: Icon(MyFlutterApp.shoe1),
            label: 'Shoes',
          ),
        ],
        selectedItemColor: Colors.red,
        onTap: (int) {},
      ),
    );
  }
}
