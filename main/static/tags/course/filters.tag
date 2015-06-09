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
