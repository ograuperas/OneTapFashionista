import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:sm_flutter/icons/one_tap_icons_icons.dart';

class BottomBar extends StatefulWidget {
  var llistaRoba;
  Function(int) Callback;
  BottomBar({this.llistaRoba, this.Callback});

  @override
  _BottomBarState createState() => _BottomBarState();
}

class _BottomBarState extends State<BottomBar> {
  int _selectedIndex = 0;
  final Map iconmap = {
    1: OneTapIcons.trousers,
    2: OneTapIcons.dress,
    3: OneTapIcons.scarf,
    4: OneTapIcons.shoes,
    5: OneTapIcons.skirt,
    6: OneTapIcons.socks,
    7: OneTapIcons.jumpsuit,
    8: OneTapIcons.tshirt,
    9: OneTapIcons.jacket,
    10: OneTapIcons.hat,
  };

  _BottomBarState();

  void _onItemTapped(int index) {
    setState(() {
      widget.Callback(widget.llistaRoba[index]['icon']);
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return BottomAppBar(
      notchMargin: 2.0,
      shape: CircularNotchedRectangle(),
      clipBehavior: Clip.antiAlias,
      child: BottomNavigationBar(
        backgroundColor: HexColor('#75CD9B'),
        type: BottomNavigationBarType.fixed,
        items: [
          ...(widget.llistaRoba.map((item) {
            print(item['icon']);
            return BottomNavigationBarItem(
              icon: Icon(iconmap[item['icon']] as IconData),
              label: item['name'],
            );
          })).toList(),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: Colors.indigo,
        onTap: _onItemTapped,
      ),
    );
  }
}
