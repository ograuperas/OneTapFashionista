import 'dart:convert';
import 'dart:typed_data';
import 'package:flex_color_picker/flex_color_picker.dart';
import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:image_gallery_saver/image_gallery_saver.dart';
import 'package:sm_flutter/Widgets/BottomBar.dart';
import 'package:sm_flutter/icons/my_flutter_app_icons.dart';
import 'dart:io';
import 'dart:ui' as ui;
import 'package:image_picker/image_picker.dart';

class ColorPickerPage extends StatefulWidget {
  static const routeName = '/colorPicker';
   @override
  _ColorPickerPageState createState() => _ColorPickerPageState();

}

class _ColorPickerPageState extends State<ColorPickerPage> {
  // Color for the picker in a dialog using onChanged.
  Color dialogPickerColor;
  final picker = ImagePicker();
  File imatge;
  var imageByte;
  Image letsgoo;

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

  Future getImageGallery () async {
    final pickedFile = await picker.getImage(source: ImageSource.gallery);
    imatge = File(pickedFile.path);
    setState(() {
      if (pickedFile != null) {
        imatge = File(pickedFile.path);
        letsgoo = Image.file(imatge);
        sendFile();
      } else {
        print('No image selected.');
      }
    });
  }
  Future<File> getImageCamera () async {
    final pickedFile = await picker.getImage(source: ImageSource.camera);
    imatge = File(pickedFile.path);
    setState(() {
      if (pickedFile != null) {
        imatge = File(pickedFile.path);
        letsgoo = Image.file(imatge);
      } else {
        print('No image selected.');
      }
    });
  }

  void sendFile() async
  {

    List<int> imageBytes = imatge.readAsBytesSync();

    final Map jsonMap = {"image": imageBytes};
    final String url = 'http://10.0.2.2:5000/getImage';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.postUrl(Uri.parse(url));
    request.headers.set('content-type', 'application/json');
    request.add(utf8.encode(json.encode(jsonMap)));
    HttpClientResponse response = await request.close();

    String reply = await response.transform(utf8.decoder).join();
   // httpClient.close();

    if (jsonDecode(reply)['res'] == 'ok') {
      print('ok');
    } else {
      print('f');
    }
  }

  void obtenirImage(BuildContext context) async {
    final String url = 'http://10.0.2.2:5000/returnImage';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.getUrl(Uri.parse(url));
    HttpClientResponse response = await request.close();
    String reply = await response.transform(utf8.decoder).join();
    //print(jsonDecode(reply)['imatge'].cast<int>());
    //File im;

    //Image aux = Image.memory(Uint8List.fromList(jsonDecode(reply)['imatge'].cast<int>()));
    //final pickedFile = await picker.getImage(source: aux);

   // File im = imatge;// = await picker.pickImage(source: aux);
    //print(Uint8List.fromList(jsonDecode(reply)['imatge'].cast<int>()));
    //await imAux.writeAsBytes(Uint8List.fromList(jsonDecode(reply)['imatge'].cast<int>()));

    setState(() {
      //imatge = imAux;//File(aux.toString());
      imageByte = Uint8List.fromList(jsonDecode(reply)['imatge'].cast<int>());
      letsgoo = Image.memory(Uint8List.fromList(jsonDecode(reply)['imatge'].cast<int>()));
    });
    //httpClient.close();

  }

  @override
  void initState() {
    super.initState();

    dialogPickerColor = Colors.red; // Material red.
  }
  int count = 0;
  void initImage(){
    if(count  < 1) {
      final int inputType = ModalRoute
          .of(context)
          .settings
          .arguments;
      if (inputType == 1) {
        getImageCamera();
      } else {
        getImageGallery();
      }
      count += 1;
    }
  }

  @override
  Widget build(BuildContext context) {
    initImage();
    return Scaffold(
      appBar: AppBar(
        title: Text('wowowow'),
        toolbarHeight: 70,
        actions: <Widget>[
          Padding(
            padding: EdgeInsets.only(right: 20.0),
            child: InkWell(
              onTap: ()  {
                ImageGallerySaver.saveFile(imageByte);

                // TODO ALERT IMAGE SAVED
              },
              child: Icon(
                Icons.save,
                size: 50,
              ),
            ),
          ),
        ],
      ),

      body: Column(children: [
        Container(
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
        ElevatedButton(onPressed:() => obtenirImage(context), child: Text('change image')),
        letsgoo == null
            ? Text('No image selected.')
            : letsgoo,

      ]),

      bottomNavigationBar: BottomBar(),
    );
  }
}
