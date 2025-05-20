// Import Firebase core and Firestore modules
console.log("app.js loaded");
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore, collection, addDoc } from "firebase/firestore";

// Your Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyAPc3JeNHvr2MwPI1NCsZyUCSNdnoISSyY",
  authDomain: "mmu-connect-8b8bd.firebaseapp.com",
  projectId: "mmu-connect-8b8bd",
  storageBucket: "mmu-connect-8b8bd.firebasestorage.app",
  messagingSenderId: "146259258589",
  appId: "1:146259258589:web:ceb98ebcf93171da913f34",
  measurementId: "G-4FQNZQJMBZ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize Firestore database
const db = getFirestore(app);

// Function to add a like document to Firestore
async function addLike(userId, postId) {
  try {
    const docRef = await addDoc(collection(db, "likes"), {
      userId: userId,
      postId: postId,
      timestamp: new Date()
    });
    console.log("Like added with ID: ", docRef.id);
  } catch (e) {
    console.error("Error adding like: ", e);
  }
}

// Call the function with sample data
addLike("user123", "post456");
