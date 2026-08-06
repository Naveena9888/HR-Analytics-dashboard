import { initializeApp } from "firebase/app";
import { getAnalytics, isSupported } from "firebase/analytics";
import {
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendPasswordResetEmail,
  signInWithPopup,
  GoogleAuthProvider,
  signOut,
  updateProfile,
  onAuthStateChanged
} from "firebase/auth";

// Firebase configuration provided by user
const firebaseConfig = {
  apiKey: "AIzaSyCLNT8AFIyn5VGTXJGxXG9FdjB2tMIL4eA",
  authDomain: "hr-analytics-dashboard-f0841.firebaseapp.com",
  projectId: "hr-analytics-dashboard-f0841",
  storageBucket: "hr-analytics-dashboard-f0841.firebasestorage.app",
  messagingSenderId: "642159325842",
  appId: "1:642159325842:web:a3d6bf6522dddd036a6c4b",
  measurementId: "G-43SCH3WKSS"
};

// Initialize Firebase App
const app = initializeApp(firebaseConfig);

// Initialize Firebase Auth & Google Provider
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();

// Initialize Analytics conditionally
export let analytics = null;
if (typeof window !== "undefined") {
  isSupported().then((supported) => {
    if (supported) {
      analytics = getAnalytics(app);
    }
  }).catch((err) => {
    console.warn("Firebase Analytics initialization skipped:", err);
  });
}

/**
 * Sign in existing user with Email and Password
 */
export async function loginWithEmail(email, password) {
  const userCredential = await signInWithEmailAndPassword(auth, email, password);
  return userCredential.user;
}

/**
 * Register new user with Email, Password, and Display Name
 */
export async function registerWithEmail(email, password, displayName) {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  if (displayName && userCredential.user) {
    await updateProfile(userCredential.user, { displayName });
  }
  return userCredential.user;
}

/**
 * Send password reset email
 */
export async function resetPassword(email) {
  await sendPasswordResetEmail(auth, email);
}

/**
 * Sign in using Google Auth Popup
 */
export async function loginWithGoogle() {
  const result = await signInWithPopup(auth, googleProvider);
  return result.user;
}

/**
 * Sign out current user
 */
export async function logoutUser() {
  await signOut(auth);
}

/**
 * Subscribe to realtime auth state changes
 */
export function subscribeToAuthChanges(callback) {
  return onAuthStateChanged(auth, callback);
}

export default app;
