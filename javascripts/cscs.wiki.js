var header='<h1>CSCS Production</h1>'
        + '<p>General repository for CSCS users</p>'
        + '<p class="view"><a href="https://github.com/eth-cscs/production">View the Project on GitHub <small>eth-cscs/production</small></a></p>'
        + '<ul>'
        + '  <li style="list-style:none"><strong>Usefull links</strong></li>'
        + '  <li><a href="https://github.com/eth-cscs/production/wiki">CSCS Production Wiki</a></li>'
        + '  <li><a href="https://github.com/eth-cscs/production/tree/master/easybuild">EasyBuild recipes</a></li>'
        + '  <li><a href="https://github.com/eth-cscs/production/tree/master/jenkins-builds">Jenkins production lists</a></li>'
        + '  <li><a target=_blank" href="https://user.cscs.ch/getting_started/compute_budget/index.html">CSCS User Portal</a></li>'
        + '  <li><a target=_blank" href="http://www.cscs.ch/index.html">CSCS web site</a></li>'
        + '</ul>'
        + '<p class="view" id="cscs-presenter-mode"><a href="#">View in presenter mode <small>refresh the browser to quit presenter mode</small></a></p>'

var footer ='<p>Project maintained by <a href="https://github.com/eth-cscs">eth-cscs</a></p>'
        + '<p>Hosted on GitHub Pages &mdash; Theme by <a href="https://github.com/orderedlist">orderedlist</a></p>'


function setupWebSiteCSCSContent()
{
    var site = ''
             + '<link rel="stylesheet" href="stylesheets/styles.css">'
             + '<link rel="stylesheet" href="stylesheets/pygment_trac.css">'
             + '<link rel="stylesheet" href="../stylesheets/styles.css">'
             + '<link rel="stylesheet" href="../stylesheets/pygment_trac.css">'
             + '  <div class="wrapper">'
             + '    <header>'
             + '    <div id="cscs-header-content">'
             + '    </div>'
             + '    </header>'
             + '    <section>      '
             + '    <div id="cscs-page-content">'
             + '    </div>'
             + '    </section>'
             + '  </div>'
             + '  <footer>'
             + '  <div id="cscs-footer-content"></div>'
             + '  <script src="../javascripts/scale.fix.js"></script>'
             + '  </footer>'
             + '  <!--[if !IE]><script>fixScale(document);</script><![endif]-->';

    document.getElementById("cscs-body-container").innerHTML = site; 
    updateWebSiteCSCSContent();
    var presenterMode = document.getElementById('cscs-presenter-mode');
    presenterMode.onclick = showCSCSPresenterMode;
}

function updateWebSiteCSCSContent()
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", CSCSContentMarkDownFile, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                var converter = new Markdown.Converter(),
                html      = converter.makeHtml(allText);

                // Replace elements
                document.getElementById("cscs-header-content").innerHTML = header;
                document.getElementById("cscs-page-content").innerHTML = html;
                document.getElementById("cscs-footer-content").innerHTML = footer;
            }
        }
    }
    rawFile.send(null);
}

function showCSCSPresenterMode() {
    var style = '' 
              // + '<style src="../stylesheets/styles.css">'
              // + '</style>'
              + '<style>'
              + '.remark-slide-content h1 {font-size: 32px;}'
              + '.remark-slide-content h2 {font-size: 32px;}'
              + '.remark-slide-content h3 {font-size: 26px;}'
              + '.remark-slide-number {right: }'
              // + '.remark-code {'
              // // + 'font-size: 11pt;'
              // + '}'
              + 'img {max-width: 100%;}'
              + 'pre {'
              + 'font-size: 12pt;'
              + 'background-color: #595959;'
              + 'color:#fff;'
              + 'border-radius:2.5px;'
              + 'overflow-x: auto;'
              + 'padding: 0.33em;'
              + '}'
              + '.remark-inline-code {'
              + 'font-size: 12pt;'
              + 'padding: 0.15em;'
              + 'border-radius:2.5px;'
              + 'font-color: $fff;'
              + 'background-color: #595959;'
              + 'color: #fff;'
              + 'margin: 0;'
              + '}'
              + '.remark-code-line {'
              + 'font-size: 12pt;'
              + 'padding: 0.15em;'
              + 'border-radius:2.5px;'
              + 'font-color: $fff;'
              + 'background-color: #595959;'
              + 'color: #fff;'
              + 'margin: 0;'
              + '}'
              + 'body {'
              + 'background-color: #fff;'
              + 'padding:0px;'
              + 'font: 13px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";'
              + 'color:#595959;'
              + 'font-weight:400;'
              + '}'
              + 'h1, h2 {'
              + '    margin-bottom: 10pt;'
              + '    margin-top: 0;'
              + '}  '
              + 'h3 {'
              + '    margin-bottom: 5pt;'
              + '    margin-top: 0;'
              + '}'
              + '</style>'
    document.getElementById("cscs-body-container").innerHTML = style;
    
    var slideshow = remark.create({sourceUrl: 'README.md'});

    document.addEventListener("keydown", keyDownTextField, false);
    function keyDownTextField(e) {
    var keyCode = e.keyCode;
      if(keyCode==27) {
        if ( $('html').hasClass('remark-container') ) {
            $('html').removeClass('remark-container');
            if ( $('body').hasClass('remark-container') ) {
                $('body').removeClass('remark-container');
                // $('body').addClass('cscs-body-container');
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
            document.getElementById("cscs-body-container").innerHTML = null;
            setupWebSiteCSCSContent();
        }
      }
    }

    slideshow.on('afterShowSlide', function (slide) {
        // if ($("div.remark-slide-number").find("div.logo").length == 0)
        // {
        //     var cscs = "<img style='width:100px' src=\"../images/cscs.jpg\" class=\"logo-img-cscs\"></img>";
        //     var logo = $("<div class=\"logo\">" + cscs + "</div>")
        //                $("div.remark-slide-number").prepend(logo);
        // }
    });
}

