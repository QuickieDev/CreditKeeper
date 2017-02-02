/**
 * Created by pav on 2/2/2017.
 */


class ApiService {
  constructor(options) {
    this.uri = options.uri;
  }

  list() {
      return $.getJSON(this.uri)
  }
}

