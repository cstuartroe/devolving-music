import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Event } from "./models";
import ResourceManager from "./ResourceManager";

type HeaderProps = {
  event: Event,
}

type HeaderState = {
  events: Event[],
}

export default class Header extends Component<HeaderProps, HeaderState>{
  constructor(props: HeaderProps) {
    super(props);

    this.state = {
      events: [],
    };
  }

  itemWidth() {
    return this.state.events.length > 1 ? 3 : 4;
  }

  componentDidMount() {
    ResourceManager.getModels("events").then(events => this.setState({events}))
  }

  renderMenuItem(to: string, text: string) {
    return (
      <div className={`col-${this.itemWidth()} menu-item`}>
        <Link to={to} className="center">
          {text}
        </Link>
      </div>
    );
  }

  render() {
    return (
      <div className="row header">
        <div className={`col-${this.itemWidth()}`}>
          <div className="header-logo">
            <Link to="/">
              {this.props.event.name.toLowerCase().replace(':', '\n')}
            </Link>
          </div>
        </div>
        {this.state.events.length > 1 && this.renderMenuItem("/event-selector", "Switch events")}
        {this.renderMenuItem("/submit-playlist", "Submit songs")}
        {this.renderMenuItem("/rate", "Rate songs")}
      </div>
    );
  }
}
