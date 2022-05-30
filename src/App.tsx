import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";

import { Event } from "./models";
import Home from "./Home";

import "../static/scss/main.scss";
import EventSelector from "./EventSelector";

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
      <div id="main-container" className="container-fluid">
        <div className="row">
          <div className="col-2"/>
          <div className="col-8">
            <Router>
              <Switch>
                {(this.state.event === null) && <>
                  <Route exact={true} path="/event_selector">
                    <EventSelector setEvent={e => {
                      this.setState({event: e})
                    }}/>
                  </Route>
                  <Redirect to={"/event_selector"}/>
                </>}
                <Route exact={true} path="/">
                  <Home event={this.state.event}/>
                </Route>
                <Redirect to="/"/>
              </Switch>
            </Router>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
