import { Component, createEffect, createSignal } from "solid-js";
import { Router, Routes, Route } from "@solidjs/router";
import SignInForm from "./forms/signin";
import Main from "./pages/main";
import SignUpForm from "./forms/signup";

export type User = {
  id: string;
  password: string;
};

const App: Component = () => {
  const [isAuth, setIsAuth] = createSignal(false);

  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Main />} />
          <Route
            path="/signIn"
            element={<SignInForm setIsAuth={setIsAuth} />}
          ></Route>
          <Route path="/signup" element={<SignUpForm />}></Route>
        </Routes>
      </Router>
      <br />
      {/* <button onclick={() => render(() => S)}>회원가입 하기</button> */}
    </div>
  );
};

export default App;
