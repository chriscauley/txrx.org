<comment-form>
  <form action={ data.form_url } method="POST" class="comment_form_wrapper { loading && 'loading' }">
    <div class="comment_form">
      <p>Comments are displayed using Markdown.</p>
      <a href="javascript:;" onclick="$(this).next().toggleClass('show')">Show Formatting help</a>
      <table class="md" cellpadding="3">
        <tbody>
          <tr style="background-color: #ffff99; text-align: center">
            <td><em>you type:</em></td>
            <td><em>you see:</em></td>
          </tr>
          <tr>
            <td>*italics*</td><td><em>italics</em></td>
          </tr>
          <tr>
            <td>**bold**</td>
            <td><b>bold</b></td>
          </tr>
          <tr>
            <td>[txrx!](http://txrxlabs.org)</td>
            <td><a href="http://txrxlabs.org">txrx!</a></td>
          </tr>
          <tr>
            <td>http://txrxlabs.org</td>
            <td><a href="http://txrxlabs.org">http://txrxlabs.org</a></td>
          </tr>
          <tr>
            <td>* item 1<br>* item 2<br>* item 3</td>
            <td><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></td>
          </tr>
          <tr>
            <td>&gt; quoted text</td>
            <td><blockquote>quoted text</blockquote></td>
          </tr>
          <tr>
            <td>Lines starting with four spaces<br>are treated like code:<br><br><span class="spaces">&nbsp;&nbsp;&nbsp;&nbsp;</span>if 1 * 2 &lt; 3:<br><span class="spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>print "hello, world!"<br></td>
            <td>Lines starting with four spaces<br>are treated like code:<br><pre>if 1 * 2 &lt; 3:<br>&nbsp;&nbsp;&nbsp;&nbsp;print "hello, world!"</pre></td>
          </tr>
        </tbody>
      </table>

      <fieldset>
        <ul class="list-unstyled">
          <li class="required">
            <textarea cols="40" id="id_comment" name="comment" rows="10">{ data.comment }</textarea>
            <input id="id_content_type" name="content_type" type="hidden" value={ data.content_type } />
            <input id="id_object_pk" name="object_pk" type="hidden" value={ data.object_pk } />
            <input id="id_parent_pk" name="parent_pk" type="hidden" value={ data.parent_pk } />
            <input id="id_comment_pk" name="comment_pk" type="hidden" value={ data.pk } />
          </li>
        </ul>
        <input type="submit" class="submit-post btn btn-primary" value="Post" onclick={ submit } />
        <input type="submit" class="submit-post btn btn-danger" value="Cancel" onclick={ cancel } />
      </fieldset>

    </div>
  </form>
  var that = this
  that.data = opts
  this.loading = false
  this.parent = opts.parent
  cancel(e) {
    this.unmount()
  }
  submit(e) {
    this.loading = true
    function callback(data) {
      if (that.parent.pk == data.pk) { // editing a comment
        var comments = that.parent.parent.parent.comments
        for (var i=0;i<comments.length;i++) {
          if (comments[i].pk == data.pk) {
            comments.splice(i,1,data)
            break
          }
        }
      } else { // new comment
        that.parent.comments.splice(0,0,data)
        that.loading = false
      }
      if (that.parent.pk) { that.unmount() }
      else {
        that.loading = false
        setTimeout(function(){window.location = '#c'+data.pk},200)
        console.log(that)
        that.comment.value = ''
      }
      riot.update()
    }
    $.post(
      this.data.form_url,
      $(this.root).find('form').serializeArray(),
      callback,
      "json"
    )
    return false;
  }
</comment-form>
