import json
import os

from IPython.display import HTML, IFrame
from jinja2 import Template

from .base_plotter import IPlotter


class DomoPhoenixPlotter(IPlotter):
    """Class for creating Domo Phoenix charts in jupyter notebook."""

    head = """
    <!-- Load Phoenix -->
    <script src='https://unpkg.com/@domoinc/domo-phoenix@latest/build/global/domoPhoenix.js'></script>
    """

    template = """
        <div id={{div_id}} style='width: 100%; height: 100%'></div>
        <script>
          var el = document.getElementById('{{div_id}}');
          var options = {
            height: {{h}} - (.15 * {{h}}),
            width: {{w}} - (.1 * {{w}}),
            colors: null
          };
          var data = {
            rows: {{data}},
            columns: {{columns}}
          };

          var interval = setInterval(function() {
            if(window.DomoPhoenix) {
              clearInterval(interval);
              var chart = new window.DomoPhoenix.Chart('{{chart_type}}', data, options);

              el.appendChild(chart.canvas);

              chart.render();
            }
          }, 10)
        </script>
    """

    def __init__(self):
        super(DomoPhoenixPlotter, self).__init__()

    def render(self,
               data,
               columns,
               chart_type,
               options=None,
               div_id="domo",
               head="",
               w=800,
               h=420):
        """Render the data in HTML template."""
        if not self.is_valid_name(div_id):
            raise ValueError(
                "Name {} is invalid. Only letters, numbers, '_', and '-' are permitted ".format(
                    div_id))

        return Template(head + self.template).render(
            div_id=div_id.replace(" ", "_"),
            data=json.dumps(
                data, indent=4).replace("'", "\\'").replace('"', "'"),
            columns=json.dumps(
                columns, indent=4).replace("'", "\\'").replace('"', "'"),
            chart_type=chart_type,
            options=json.dumps(
                options, indent=4).replace("'", "\\'").replace('"', "'"),
            w=w,
            h=h)

    def plot(self, data, columns, chart_type, options=None, w=800, h=420):
        """Output an iframe containing the plot in the notebook without saving."""
        return HTML(
            self.iframe.format(
                source=self.render(
                    data=data,
                    columns=columns,
                    chart_type=chart_type,
                    options=options,
                    head=self.head,
                    w=w,
                    h=h),
                w=w,
                h=h))
