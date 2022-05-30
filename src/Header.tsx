import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Event } from "./models";

type HeaderProps = {
  event: Event,
}

export default class Header extends Component<HeaderProps, {}>{
  constructor(props: HeaderProps) {
    super(props);
  }

  renderMenuItem(to: string, text: string) {
    return (
      <div className="col-3 menu-item">
        <Link to={to}>
          {text}
        </Link>
      </div>
    );
  }

  render() {
    return (
      <div className="row header">
        <div className="col-3">
          <div className="header-logo">
            <Link to="/">
              {this.props.event.name.toLowerCase().replace(':', '\n')}
            </Link>
          </div>
        </div>
        {this.renderMenuItem("/event-selector", "Switch events")}
        {this.renderMenuItem("/submit-playlist", "Submit songs")}
        {this.renderMenuItem("/rate", "Rate songs")}
      </div>
    );
  }
}
