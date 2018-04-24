class CustomURLSearchParams {
  constructor(search) {
    let entries = search.entries(), el = null, q = []

    do {
      el = entries.next().value
      if (el) {
        this.appendTo(q, el[0], el[1])
      }
    } while (el)
    this.params = q
  }

  appendTo(dict, name, value) {
    var val = typeof value === 'string' ? value : (
      value !== null && typeof value.toString === 'function' ? value.toString() : JSON.stringify(value)
    )

    if (name in dict) {
      dict[name].push(val)
    } else {
      dict[name] = [val]
    }
  }

  toString() {
    var dict = this.params, query = [], i, key, name, val
    for (key in dict) {
      name = this.encode(key)
      for (i = 0, val = dict[key]; i < val.length; i++) {
        query.push(name + '=' + this.encode(val[i]))
      }
    }
    return query.join('&')
  }

  encode(str) {
    var replace = {
      '!': '%21',
      '\'': '%27',
      '(': '%28',
      ')': '%29',
      '~': '%7E',
      '%20': '+',
      '%00': '\x00'
    }
    return encodeURIComponent(str).replace(/[!'()~]|%20|%00/g, function (match) {
      return replace[match]
    })
  }
}

export default CustomURLSearchParams
