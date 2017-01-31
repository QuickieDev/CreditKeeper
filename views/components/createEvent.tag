<create-event>
    <div class="modal fade" id="createModal" tabindex="-1" role="dialog" aria-labelledby="createModalLabel">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h4 class="modal-title" id="myModalLabel">Create new Event</h4>
          </div>
          <div class="modal-body">
            'Insert stuff ...'
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary">Save changes</button>
          </div>
        </div>
      </div>
    </div>

    // component Attributes

    this.calendar = this.opts.calendar
    this.event = {}
    this.modal = $(this.createModal)

    var self = this

    // methods

    // events

    this.calendar.on('createEvent', function(event) {
        self.modal.modal('show')
    })

</create-event>