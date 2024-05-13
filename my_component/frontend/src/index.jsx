import React from "react"
import MyComponent from "./MyComponent"
import { createRoot } from 'react-dom/client';
// import Xest from "./Xest"

import { render } from 'react-dom';

import { ClerkProvider} from '@clerk/clerk-react';

const publishableKey = process.env.VITE_CLERK_PUBLISHABLE_KEY || "pk_test_cHJpbWUtc2hyaW1wLTQwLmNsZXJrLmFjY291bnRzLmRldiQ";

// render(
//   <ClerkProvider publishableKey={publishableKey}>
//     <MyComponent />
//   </ClerkProvider>,
//   document.getElementById('root'),
// );

// function App() {
//   return (
//     <>
//       <h1>Hello Clerk!</h1>
//       <SignedIn>
//         <UserButton afterSignOutUrl={window.location.href} />
//       </SignedIn>
//       <SignedOut>
//         <SignInButton mode='modal' />
//       </SignedOut>
//     </>
//   );
// }
// console.log("xxx")
const container = document.getElementById('root');

const root = createRoot(container);

root.render(
    <ClerkProvider publishableKey={publishableKey}>
    <MyComponent />
    </ClerkProvider>
)

// console.log("xxx1")
