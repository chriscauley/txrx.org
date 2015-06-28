<course-filters>
  <input type="checkbox" id="toggle_filters" name="toggle"/>
  <label for="toggle_filters" class="btn btn-success">Filter by Subject</label>
  <form onsubmit={ apply } class="filters course_filters" autocomplete="off">
    <input name="q" class="form-control" placeholder="Search Classes" onkeyup={ search } 
           onblur={ apply } id="courseSearch" />
    <div class="list_filter btn-group-vertical">
      <label class="btn btn-default { opts.active_subject?' ':'selected' }" onclick={ click }>All Subjects</label>
    </div>
    <div each={ CLASS_SUBJECTS } class="list_filter btn-group-vertical">
      <label if={ active_courses + inactive_courses } onclick={ parent.click }
             class="btn btn-default { (parent.opts.active_subject == value)?'selected':' ' }" >{ name }</label>
      <!--
          <div each={ children } class="child">
            <input type="radio" value={ value } id="filter_subject_{ value }" name="subject" />
            <label for="filter_subject_{ value }" class="btn btn-default" onclick={ filter }>-- { name }</label>
          </div>
          -->
    </div>
  </form>

  click(e) {
    opts.filterSubjects(e.item?e.item.value:"");
    opts.active_subject = e.item.value;
    this.toggle.checked = false;
    riot.update();
  }
  apply(e) {
    opts.filterSearch(this.q.value);
    this.toggle.checked = false;
    riot.update();
  }
  search(e) {
    opts.filterSearch(this.q.value);
    riot.update();
  }
</course-filters>
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
      <div class="price">{ (fee > 0 && next_time != 0)?("$"+fee):"FREE" }</div>
    </a>
  </div>
</course-list>
