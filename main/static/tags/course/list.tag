<course-list>
  <div each={ opts.courses }>
    <a href={ url } class="course well { well_class }" id="c{ id }">
      <div class="picture">
        <img src={ im.url } width={ im.width } height={ im.height } />
        <div class="enrolled-status" status={ enrolled_status }></div>
      </div>
      <div class="details">
        <div class="subjects"><span each={ subject }>{ subject }</span></div>
        <div class="title">{ name }</div>
        <div class="description">{ short_description }</div>
        <div class="enrolled-status" data-status={ enrolled_status }></div>
        <div class="sessions" if={ active_sessions.length }>
          <span class="next_session { active_sessions[0].closed_status }">{ active_sessions[0].short_dates }</span>
          <div class="pull-right">
            <span class="full_sessions" if={ full_sessions.length }>
              [{ full_sessions.length } Full<span class=" hidden-xs"> Session{ (full_sessions.length > 1)?"s":"" }</span>]
            </span>
            <span class="open_sessions" if={ open_sessions.length }>
              [{ open_sessions.length } Open<span class=" hidden-xs"> Session{ (open_sessions.length > 1)?"s":"" }</span>]
            </span>
          </div>
        </div>
      </div>
      <div class="price" if={ fee === 0 || fee }>{ (fee > 0 && next_time != 0)?("$"+fee):"FREE" }</div>
    </a>
  </div>
</course-list>
