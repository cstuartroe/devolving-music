import React, { Component } from "react";
import { Event } from "./models";
import EventSelector, { event_setter } from "./EventSelector";

type HomeProps = {
  event: Event | null,
  setEvent: event_setter,
}

export default class Home extends Component<HomeProps, {}> {
  render() {
    if (this.props.event === null) {
      return <EventSelector setEvent={this.props.setEvent}/>
    } else {
      return (
        <div>
          {}
        </div>
      );
    }
  }
}
