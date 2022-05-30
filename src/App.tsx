import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import { Event } from "./models";
import Home from "./Home";

import "../static/scss/main.scss";

type AppState = {
  event: Event | null,
}

class App extends Component<{}, AppState> {
  constructor(props: {}) {
    super(props);

    this.state = {
      event: null,
    };
  }

  render() {
    return (
      <Router>
        <Switch>
          <Route exact={true} path="/">
            <Home event={this.state.event} setEvent={e => this.setState({event: e})}/>
          </Route>
        </Switch>
      </Router>
    );
  }
}

export default App;
