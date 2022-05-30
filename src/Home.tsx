import React, { Component } from "react";
import { Event } from "./models";

type HomeProps = {
  event: Event,
}

export default class Home extends Component<HomeProps, {}> {
  render() {
    return (
      <>
        <p>
          Welcome to the Devolving Party music voting site!
        </p>

        <p>
          Try one of the above links to take an action or{' '}
          <a href="http://devolving.party">click here</a>
          {' '}to learn more about Devolving.
        </p>
      </>
    );
  }
}
