<edit-event>
    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h4 class="modal-title" id="myModalLabel">{ event.title }</h4>
          </div>
          <div class="modal-body">
            { event.description }
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" onclick={ editEvent } >Save changes</button>
          </div>
        </div>
      </div>
    </div>

    // component Attributes

    this.calendar = this.opts.calendar
    this.event = {}
    this.modal = $(this.myModal)
    this.index = 0

    var self = this

    // methods

    editEvent(event) {
        //self.calendar.trigger('updateEvent', {})
        self.index++
        console.log('Edit Event occurred: ', self.index)
        self.calendar.proxy.fullCalendar('refetchEvents');

        //modal = $(self.myModal)
        //modal.modal('hide')
        self.modal.modal('hide')
    }


    // events

    this.calendar.on('editEvent', function(event) {
        self.event = event
        self.update()
        self.modal.modal('show')
    })


</edit-event>