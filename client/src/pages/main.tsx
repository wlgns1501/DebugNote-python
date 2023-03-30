import { Component, createSignal, Switch } from "solid-js";

interface MainProps {
  isAuth: any;
}

const Main: Component<MainProps> = (props) => {
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
