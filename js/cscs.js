var __cscsSiteNavBar = "";
var __cscsSiteContainter = "";
var __cscsMarkDown = "";

function cscs_read_file_contents(filename, callback) 
{
  var rawFile = new XMLHttpRequest();
  rawFile.open("GET", filename, false);

  var __fileContent = "";
  rawFile.onreadystatechange = function ()
  {
      if(rawFile.readyState === 4) {
          if(rawFile.status === 200 || rawFile.status == 0) {
              __fileContent = rawFile.responseText;
              if(typeof callback == 'function'){
                callback(__fileContent);
              }
          }
      }
  }
  rawFile.send(null);
}

function cscs_setup_site_content(navbarfile, containerfile) {
  __cscsSiteNavBar = navbarfile;
  __cscsSiteContainter = containerfile;
  
  cscs_read_file_contents(navbarfile, function __populate_site_content(argument) {
    document.getElementById("cscs-site-content").innerHTML = argument;
  });

  cscs_read_file_contents(containerfile, function cscs_populate_site_content(argument) {
    document.getElementById("cscs-site-content").innerHTML += argument;
  });

  var presenterMode = document.getElementById('start-cscs-presenter-mode');
  presenterMode.click(function(e){e.preventDefault();});
  presenterMode.onclick = __cscs_show_in_presenter_mode;

  __cscs_email_protector();
}
      
function cscs_setup_markdown_page_content(markdownFile)
{
  __cscsMarkDown = markdownFile;

  cscs_read_file_contents(markdownFile, function __populate_site_content(argument) {

  // var marked = require('marked');
  marked.setOptions({
    gfm: true,
    tables: true,
    breaks: false,

    // Without this set to true, converting something like
    // <p>*</p><p>*</p> will become <p><em></p><p></em></p>
    pedantic: true,

    sanitize: false,
    smartLists: true,
    langPrefix: '',
    // highlight: function (code) {
    //   return hljs.highlightAuto(code).value;
    // }    
  });

    // converting markdown to html
    // var converter = new Markdown.Converter();
    // document.getElementById("cscs-markdown-content").innerHTML = converter.makeHtml(argument);
    // document.getElementById("cscs-markdown-content").innerHTML = marked(argument);
    marked(argument, function (err, content) {
      if (err) throw err;
      document.getElementById("cscs-markdown-content").innerHTML = content;
    });

  });
}      

function cscs_setup_index_page_content(newsfile)
{
  cscs_read_file_contents(newsfile, function __populate_site_content(argument) {
    // converting markdown to html
    // var converter = new Markdown.Converter();
    // document.getElementById("cscs-markdown-content").innerHTML = converter.makeHtml(argument);
    marked(argument, function (err, content) {
      if (err) throw err;
      document.getElementById("cscs-markdown-content").innerHTML = content;
    });    
  });

  cscs_read_file_contents("https://raw.githubusercontent.com/eth-cscs/production/master/jenkins-builds/6.0.UP02-2016.11-gpu", function __populate_site_content(argument) {
    document.getElementById("cscs-markdown-content").innerHTML += '<h2>Daint GPU partition</h2><pre>' + argument + '</pre>';
  });

  cscs_read_file_contents("https://raw.githubusercontent.com/eth-cscs/production/master/jenkins-builds/6.0.UP02-2016.11-mc", function __populate_site_content(argument) {
    document.getElementById("cscs-markdown-content").innerHTML += '<h2>Daint MC partition</h2><pre>' + argument + '</pre>';
  });
}      


function __cscs_show_in_presenter_mode() {
  document.getElementById("cscs-body-container").innerHTML = null;

  var slideshow = remark.create({sourceUrl: __cscsMarkDown});

  document.addEventListener("keydown", keyDownEscapePresenterMode, false);
  function keyDownEscapePresenterMode(e) {
    var keyCode = e.keyCode;
    if(keyCode == 27) {
      __cscs_exit_presentation_mode();
    }
  }
  // the click blocks, so forcing full page reload for the click
  var presenterMode = document.getElementById('start-cscs-presenter-mode');
  presenterMode.style.display = 'none';
  var exitMode = document.getElementById('exit-cscs-presenter-mode');
  exitMode.style.display = 'block';

  // workaround to work for local and non local servers
  if(document.location.domain == null)
    exitMode.href = document.location.pathname;
  else
    exitMode.href = document.location.domain+document.location.pathname;

  slideshow.on();
}

// This function destroys the remark presentation and restores the CSCS website
function __cscs_exit_presentation_mode() {
  if ( $('html').hasClass('remark-container') ) {
      $('html').removeClass('remark-container');
      if ( $('body').hasClass('remark-container') ) {
          $('body').removeClass('remark-container');
      }
      if ( $('body').hasClass('remark-presenter-mode') ) {
          $('body').removeClass('remark-presenter-mode');
      }
      if ($(".remark-notes-area").length > 0) {
          $(".remark-notes-area").remove();
      }
      if ($(".remark-slides-area").length > 0) {
          $(".remark-slides-area").remove();
      }
      if ($(".remark-preview-area").length > 0) {
          $(".remark-preview-area").remove();
      }
      if ($(".remark-backdrop").length > 0) {
          $(".remark-backdrop").remove();
      }
      if ($(".remark-help").length > 0) {
          $(".remark-help").remove();
      }
      if ($(".remark-pause").length > 0) {
          $(".remark-pause").remove();
      }
      document.getElementById("cscs-site-content").innerHTML = null;
      cscs_setup_site_content(__cscsSiteNavBar, __cscsSiteContainter);
      cscs_setup_markdown_page_content(__cscsMarkDown);      
  }
}

function __cscs_email_protector() {
  $("#cscs-email-protector").prepend('<a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;%69%6E%66%6F%40%63%73%63%73%2E%63%68">Contact us</a>');
}
