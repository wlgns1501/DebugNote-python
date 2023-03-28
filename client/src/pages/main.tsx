import { Component, createSignal } from "solid-js";

const Main: Component = () => {
  const [isAuth, setIsAuth] = createSignal(false);

  return (
    <div>
      <h1>debugnote</h1>
      <div>
        <a href="/signin">로그인</a>
        <br />
        <a href="/signup">회원가입</a>
      </div>
    </div>
  );
};

export default Main;
