import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:journal_app/screens/loginsignup/login.dart';
import 'package:journal_app/screens/mentees.dart';
import 'package:shared_preferences/shared_preferences.dart';

class teacherscreen extends StatefulWidget {
  const teacherscreen({super.key});

  @override
  State<teacherscreen> createState() => _teacherscreenState();
}

class _teacherscreenState extends State<teacherscreen> {
  String? username;
  String? name;
  String? selectedDocumentId;

  @override
  void initState() {
    super.initState();
    _loadSharedPrefs(); // Load the QR code image when the home page is initialized
  }

  _loadSharedPrefs() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      username = prefs.getString('username');
      name = prefs.getString('name');
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.lightBlue,
        title: const Text('Mentor Home'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              signout(context);
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            const SizedBox(
              height: 30,
            ),
            SizedBox(
              width: double.infinity,
              child: Text(
                'Welcome $name,',
                style: const TextStyle(fontSize: 45, fontWeight: FontWeight.bold),
                textAlign: TextAlign.left,
              ),
            ),
            const SizedBox(
              height: 30,
            ),
            SizedBox(height: 20),
            StreamBuilder(
              stream: FirebaseFirestore.instance.collection('class').snapshots(),
              builder: (BuildContext context, AsyncSnapshot<QuerySnapshot> snapshot) {
                if (!snapshot.hasData) {
                  return CircularProgressIndicator();
                }
                List<String> documentIds = snapshot.data!.docs.map((doc) => doc.id).toList();
                return Column(
                  children: [
                    DropdownButton(
                       underline: Container(
                          height: 2,
                          color: Colors.deepPurpleAccent,
                        ),
                        elevation: 16,
                      value: selectedDocumentId,
                      onChanged: (String? newValue) {
                        setState(() {
                          selectedDocumentId = newValue;
                        });
                      },
                      hint: Align(
                        alignment: Alignment.centerRight,
                        child: Text(
                          "Select Class to view mentees",
                          style: TextStyle(color: Colors.black87),
                        ),
                      ),
                      items: documentIds.map<DropdownMenuItem<String>>((String value) {
                        return DropdownMenuItem<String>(
                          value: value,
                          child: Text(value),
                        );
                      }).toList(),
                    ),
                    SizedBox(height: 20),
                   ElevatedButton(
  onPressed: () {
    if (selectedDocumentId == null) {
      // Show a message to select an item
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Please select an item from the dropdown.'),
        ),
      );
    } else {
      // Navigate to another screen with the selected item as an argument
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => AnotherScreen(selectedItem: selectedDocumentId!),
        ),
      );
    }
  },
  child: Text('Submit'),
),

                  ],
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  signout(BuildContext ctx) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    Navigator.of(ctx).pushAndRemoveUntil(
      MaterialPageRoute(builder: (ctx1) => LoginScreen2()),
      (route) => false,
    );
  }
}
