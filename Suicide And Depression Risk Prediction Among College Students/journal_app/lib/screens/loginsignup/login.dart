//import 'package:busti007/screens/singup_conductor.dart';
// import 'package:bus_t/screens/loginsignup/singup_conductor.dart';
import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:journal_app/screens/homescreen.dart';
import 'package:journal_app/screens/teacherscreen.dart';
import 'package:shared_preferences/shared_preferences.dart';

// import '../conductor/c_home.dart';

//import 'c_home.dart';

class LoginScreen2 extends StatelessWidget {
  final TextEditingController uidController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  LoginScreen2({super.key});
  Future<void> _storeDocumentIdInSharedPreferences(String documentId,String role,String classname,String name) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('username', documentId);
    await prefs.setString('role', role);
    await prefs.setString('classname', classname);
    await prefs.setString('name', name);
  }
  void login(BuildContext context) async {
    try {
      String uid = uidController.text;
      String password = passwordController.text;
        
      // Check if the provided bus ID exists in Firestore
      QuerySnapshot<Map<String, dynamic>> querySnapshot = await FirebaseFirestore.instance
          .collection('users')
          .where('id', isEqualTo: uid)
          .get();

      if (querySnapshot.docs.isEmpty) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Invalid  ID or password'),
          ),
        );
        return;
      }

      // Get the first document from the query result
      DocumentSnapshot<Map<String, dynamic>> documentSnapshot = querySnapshot.docs.first;

      // Verify the password
      String storedPassword = documentSnapshot.get('password');
      if (password != storedPassword) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Invalid  username or password'),
          ),
        );
        return;
      }
      String role = documentSnapshot.get('role');
      String classname = documentSnapshot.get('class');
      String name = documentSnapshot.get('name');
       final busno = uid;
       _storeDocumentIdInSharedPreferences(busno,role,classname,name);
      // Login successful
      // Perform additional actions if needed

      if(role == 'student'){
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (ctx1) =>  HomeScreen()),);
    }
    else if(role == 'teacher'){
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (ctx1) =>  teacherscreen()),);
    }
    } catch (error) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Login failed: ${error.toString()}'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Enter login details'),
        backgroundColor: Colors.blue,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: uidController,
              decoration: const InputDecoration(labelText: 'Username'),
            ),
            TextField(
              controller: passwordController,
              decoration: const InputDecoration(labelText: 'Password'),
              obscureText: true,
            ),
            ElevatedButton(
              onPressed: () {
                login(context);
              },
              child: const Text('Login'),
            ),
            const SizedBox(height: 16),
            // GestureDetector(
            //   onTap: () {
            //     // Navigator.push(
            //     //   context,
            //     //   MaterialPageRoute(builder: (context) => const SignUpConductor()),
            //     // );
            //   },
            //   child: const Text(
            //     'Don\'t have an account? Sign up',
            //     style: TextStyle(
            //       color: Colors.blue,
            //       fontWeight: FontWeight.bold,
            //     ),
            //   ),
            // ),
          ],
        ),
      ),
    );
  }
}