// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables, avoid_print
import 'package:flutter/material.dart';
import 'package:journal_app/components.dart';
import '../constants.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:intl/intl.dart';

class AddEntryScreen extends StatefulWidget {
  final String? username;
  final String? classname;
  const AddEntryScreen({Key? key,required this.username,required this.classname}) : super(key: key);

  @override
  State<AddEntryScreen> createState() => _AddEntryScreenState();
}

class _AddEntryScreenState extends State<AddEntryScreen> {
  TextEditingController titleControl = TextEditingController();
  TextEditingController entryControl = TextEditingController();
  @override
  Widget build(BuildContext context) {
    final w = MediaQuery.of(context).size.width;
    return SafeArea(
      child: Scaffold(
        resizeToAvoidBottomInset: false,
        body: Container(
          width: double.infinity,
          height: double.infinity,
          decoration: kScreenBg,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              SizedBox(
                height: 10,
              ),
              JournyTitle(),
              SizedBox(
                height: 10,
              ),
              Container(
                width: w * 0.8,
                padding: EdgeInsets.symmetric(
                  vertical: 3,
                  horizontal: 10,
                ),
                decoration: kTextField,
                child: Center(
                  child: TextFormField(
                    controller: titleControl,
                    cursorColor: Colors.white,
                    style: TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.w600,
                      color: Colors.white,
                    ),
                    decoration: InputDecoration(
                      border: InputBorder.none,
                      hintText: 'Entry Title*',
                      hintStyle: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w600,
                        color: Colors.white.withOpacity(0.7),
                      ),
                    ),
                  ),
                ),
              ),
              SizedBox(
                height: 15,
              ),
              Expanded(
                child: Container(
                  width: w * 0.8,
                  padding: EdgeInsets.symmetric(
                    vertical: 3,
                    horizontal: 10,
                  ),
                  decoration: BoxDecoration(
                    border: Border.all(
                      width: 2.5,
                      color: Colors.white,
                    ),
                    borderRadius: BorderRadius.all(
                      Radius.circular(
                        15,
                      ),
                    ),
                  ),
                  child: SingleChildScrollView(
                    reverse: entryControl.text.length > 20 ? true : false,
                    child: Center(
                      child: TextFormField(
                        controller: entryControl,
                        cursorColor: Colors.white,
                        maxLines: 15,
                        keyboardType: TextInputType.multiline,
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 25,
                        ),
                        decoration: InputDecoration(
                          border: InputBorder.none,
                          hintText: 'Create new Entry',
                          hintStyle: TextStyle(
                            color: Colors.white.withOpacity(0.4),
                            fontSize: 25,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              SizedBox(
                height: 20,
              ),
              JournyButton(
                  label: "SAVE",
                  fn: () async {
                    if (titleControl.text.isEmpty ||
                        entryControl.text.isEmpty) {
                      showTextEmptyAlert(context);
                    } else {
                      final path = 'diary/${widget.classname}/${widget.username}/recent';
                      final path1 = 'diary/${widget.classname}/${widget.username}/history/history';
                      final path2 = 'diary/${widget.classname}/${widget.username}/verification';
                      final path3 = 'class/${widget.classname}';
                      await FirebaseFirestore.instance
                          .collection(path1)
                          .add({
                            'Title': titleControl.text,
                            'Entry': entryControl.text,
                            'Date': DateFormat.yMMMEd()
                                .add_jm()
                                .format(DateTime.now()),
                          })
                          .then((value) => showFireBaseAlert(context))
                          .catchError((error) => showErrorAlert());
                           await FirebaseFirestore.instance.doc(path2).update({
                            'verification': 0,
                               });
                               await FirebaseFirestore.instance.doc(path3).update({
                            'verification': 0,
                               });
                               await FirebaseFirestore.instance.doc(path).update({
                            'recent': entryControl.text,
                               });
                      titleControl.clear();
                      entryControl.clear();
                    }
                  }),
              SizedBox(
                height: 40,
              ),
            ],
          ),
        ),
      ),
    );
  }

  showFireBaseAlert(BuildContext context) {
    Widget okButton = TextButton(
      onPressed: () {
        Navigator.pop(context);
      },
      child: Text('OK'),
    );
    AlertDialog alert = AlertDialog(
      title: Text('Data upload Status'),
      content: Text("Entry added Successfully"),
      actions: [
        okButton,
      ],
    );
    showDialog(
        context: context,
        builder: (context) {
          return alert;
        });
  }

  showTextEmptyAlert(BuildContext context) {
    Widget okButton = TextButton(
      onPressed: () {
        Navigator.pop(context);
      },
      child: Text('OK'),
    );
    AlertDialog alert = AlertDialog(
      title: Text('Empty entry'),
      content: Text("Please enter title and entry"),
      actions: [
        okButton,
      ],
    );
    showDialog(
        context: context,
        builder: (context) {
          return alert;
        });
  }

  showErrorAlert() {
    Widget okButton = TextButton(
      onPressed: () {
        Navigator.pop(context);
      },
      child: Text('OK'),
    );
    AlertDialog alert = AlertDialog(
      title: Text('Something Went wrong'),
      content: Text("Entry not added due to an error"),
      actions: [
        okButton,
      ],
    );
    showDialog(
        context: context,
        builder: (context) {
          return alert;
        });
  }

  @override
  void dispose() {
    // TODO: implement dispose
    titleControl.dispose();
    entryControl.dispose();
    super.dispose();
  }
}