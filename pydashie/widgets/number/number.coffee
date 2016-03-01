class Dashing.Number extends Dashing.Widget
  @accessor 'current', Dashing.AnimatedValue

  @accessor 'difference', ->
    if @get('last')
      last = parseInt(@get('last'))
      current = parseInt(@get('current'))
      if last != 0
        diff = Math.abs(Math.round((current - last) / last * 100))
        "#{diff}%"
    else
      ""

  @accessor 'moreinfo', ->
    diff = @get('more-info')
    "#{diff}"

  @accessor 'arrow', ->
    if @get('last')
      #if parseInt(@get('current')) > parseInt(@get('last')) then '+' else '-'
      if parseInt(@get('current')) > parseInt(@get('last')) then '\u25B2' else '\u25BC'
      #if parseInt(@get('current')) > parseInt(@get('last')) then 'icon-arrow-up' else 'icon-arrow-down'

  onData: (data) ->
    console.log($(@get('node')))
    console.log($(@node))

    if @get('alarm') == true
        $(@node).context.style.backgroundColor='darkred'
    else
        $(@node).context.style.cssText=''

    console.log($(@node).context.style)

    if data.status
      $(@get('node')).addClass("status-#{data.status}")