import { Component } from "solid-js";

const SignUpForm: Component = () => {
  return (
    <div>
      <h1>회원가입</h1>
      <form>
        id : <input></input>
        <br></br>
        password : <input></input>
        <br></br>
        checkPassword : <input></input>
        <br></br>
        nickname : <input></input>
        <br></br>
      </form>
    </div>
  );
};

export default SignUpForm;
