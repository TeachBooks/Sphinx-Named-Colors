import os
from sphinx.application import Sphinx
import numpy as np
from docutils import nodes
from docutils.writers import Writer
from sphinx.util.docutils import SphinxRole
from docutils.parsers.rst.directives.admonitions import Admonition
import sphinxnotes.comboroles as spcr

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def calc_mid_and_min(rgb):

    # convert to hex
    hex = rgb_to_hex(rgb)
    hex_mid = hex+'20'
    hex_min = hex+'05'

    return hex_mid, hex_min

def hue_rotate(rgb,angle):
    # angle must be in degrees

    rgb = np.array(rgb)

    A1 = np.array([[0.213,0.715,0.072],[0.213,0.715,0.072],[0.213,0.715,0.072]])
    A2 = np.array([[0.787,-0.715,-0.072],[-0.213,0.285,-0.072],[-0.213,-0.715,0.928]])
    A3 = np.array([[-0.213,-0.715,0.928],[0.143,0.140,-0.283],[-0.787,0.715,0.072]])

    A = A1 + np.cos(np.deg2rad(angle))*A2+np.sin(np.deg2rad(angle))*A3

    rgb = A@rgb
    rgb = np.round(rgb).astype(int)
    rgb[rgb>255] = 255
    rgb[rgb<0] = 0

    return list(rgb)

def saturate(rgb,sat):
    # sat must be scalar

    rgb = np.array(rgb)

    A1 = np.array([[0.213,0.715,0.072],[0.213,0.715,0.072],[0.213,0.715,0.072]])
    A2 = np.array([[0.787,-0.715,-0.072],[-0.213,0.285,-0.072],[-0.213,-0.715,0.928]])
    
    A = A1 + sat*A2

    rgb = A@rgb
    rgb = np.round(rgb).astype(int)
    rgb[rgb>255] = 255
    rgb[rgb<0] = 0
    
    return list(rgb)

def write_css(app,exc):

    list_of_colors = app.config.named_colors_custom_colors
    if list_of_colors is not None:
    # generate list of names
        names = list(list_of_colors.keys())
        # get rgb code for light colors
        light_colors = {}
        for name in names:
            rgb = list_of_colors[name][0:3]
            light_colors[name] = rgb_to_hex(rgb)
            hex_mid, hex_min = calc_mid_and_min(rgb)
            light_colors[name+'-mid'] = hex_mid
            light_colors[name+'-min'] = hex_min
        # if dark colors are required, get/generate them
        if app.config.named_colors_dark_and_light:
            # assumption: get overrules generate
            dark_colors = {}
            for name in names:
                if len(list_of_colors[name])>3:
                    # get
                    rgb = list_of_colors[name][3:]
                else:
                    # generate
                    # 1) invert
                    rgb = [255-c for c in list_of_colors[name][0:3]]
                    # 2) rotate hue
                    rgb = hue_rotate(rgb,180)
                    # 3) saturate
                    rgb = saturate(rgb,app.config.named_colors_saturation)
                dark_colors[name] = rgb_to_hex(rgb)
                hex_mid, hex_min = calc_mid_and_min(rgb)
                dark_colors[name+'-mid'] = hex_mid
                dark_colors[name+'-min'] = hex_min

        # now set the CSS
        CSS_content = ''
        # light color string
        CSS_light = '/* (light/default mode) colors */\n:root {'
        for name in light_colors:
            CSS_light += '\n\t--%s: %s;'%(name,light_colors[name])
        CSS_light += '\n}'
        CSS_content += CSS_light+'\n\n'
        # dark color string
        if app.config.named_colors_dark_and_light:
            CSS_dark = '/* dark mode colors */\nhtml[data-theme="dark"] {'
            for name in dark_colors:
                CSS_dark += '\n\t--%s: %s;'%(name,dark_colors[name])
            CSS_dark += '\n}'
            CSS_content += CSS_dark+'\n\n'
        # class strings
        CSS_class = '/* LaTeX classes */\n'
        for name in names:
            CSS_class += '.%s {color: var(--%s);}\n'%(name,name)
        CSS_content += CSS_class+'\n\n'
        # admonitions
        base = '/* <color> */\ndiv.admonition.<color> {\n\tborder-color: var(--<color>);\n\tbackground-color: var(--<color>-min);\n}\n'
        base += 'div.admonition.<color> > .admonition-title {\n\tcolor: var(--pst-color-text-base);\n\tbackground-color: var(--<color>-mid);\n}\n'
        base += 'div.admonition.<color> > .admonition-title::after {\n\tcolor: var(--<color>);\n}\n'
        base += 'div.admonition.<color> > p,\ndiv.admonition.<color> > section {\n\tcolor: var(--pst-color-text-base);\n}\n'
        CSS_admonitions = '/* Admonition classes */\n'
        for name in names:
            CSS_admonitions += base.replace('<color>',name)
        CSS_content += CSS_admonitions
        # add no-title stuff
        CSS_notitle = "/* no-title class */\n"
        CSS_notitle += "div.admonition.no-title > .admonition-title {\n\tdisplay: none;\n}\n"
        CSS_notitle += "div.admonition.no-title.dropdown > .admonition-title {\n\tvisibility: hidden;\n}\n"
        CSS_content += CSS_notitle
        # write the css file
        staticdir = os.path.join(app.builder.outdir, '_static')
        filename = os.path.join(staticdir,'tb_cc.css')
        with open(filename,"w") as css:
            css.write(CSS_content)

    return

def set_latex(app,conf):

    old =  app.config

    if old.named_colors_custom_colors is not None:
        for name in old.named_colors_custom_colors:
            newcommand_name = name
            newcommand_content = ['\class{%s}{#1}'%(name),1]
            
            if 'mathjax3_config' in old:
                old_mj = old.mathjax3_config
                if old_mj is None:
                    old['mathjax3_config'] = {'tex': {'macros': {newcommand_name: newcommand_content}}}
                elif 'tex' in old_mj:
                    old_mj_tex = old.mathjax3_config['tex']
                    if 'macros' in old_mj_tex:
                        old_mj_tex['macros'] = old_mj_tex['macros'] | {newcommand_name: newcommand_content}
                        old.mathjax3_config['tex'] = old_mj_tex
                    else:
                        old.mathjax3_config['tex'] = old.mathjax3_config['tex'] | {'macros': {newcommand_name: newcommand_content}}
                else:
                    old.mathjax3_config['tex'] = {'macros': {newcommand_name: newcommand_content}}
            else:
                old['mathjax3_config'] = {'tex': {'macros': {newcommand_name: newcommand_content}}}
            
        app.config = old

    return

def setup(app: Sphinx):

    app.setup_extension('sphinxnotes.comboroles')

    app.add_config_value('named_colors_custom_colors', None, 'env')
    app.add_config_value('named_colors_dark_and_light', True, 'env')
    app.add_config_value('named_colors_saturation', 1.5, 'env')
    app.add_config_value('named_colors_include_CSS', True, 'env')

    app.add_css_file('tb_cc.css')

    app.connect('config-inited',set_named)
    app.connect('config-inited',set_latex)
    app.connect('config-inited',spcr._config_inited)

    app.add_node(ColorText, html=(visit_color_text, depart_color_text))

    app.connect("build-finished",write_css)

    return

def set_named(app,conf):

    old =  app.config

    if old.named_colors_include_CSS:


        # list of named colors from
        # https://developer.mozilla.org/en-US/docs/Web/CSS/named-color
        named_colors = {
            'black':[0,0,0],
            'silver':[192,192,192],
            'gray':[128,128,128],
            'white':[255,255,255],
            'maroon':[128,0,0],
            'red':[255,0,0],
            'purple':[128,0,128],
            'fuchsia':[255,0,255],
            'green':[0,128,0],
            'lime':[0,255,0],
            'olive':[128,128,0],
            'yellow':[255,255,0],
            'navy':[0,0,128],
            'blue':[0,0,255],
            'teal':[0,128,128],
            'aqua':[0,255,255],
            'aliceblue':[240,248,255],
            'antiquewhite':[250,235,215],
            'aqua':[0,255,255],
            'aquamarine':[127,255,212],
            'azure':[240,255,255],
            'beige':[245,245,220],
            'bisque':[255,228,196],
            'black':[0,0,0],
            'blanchedalmond':[255,235,205],
            'blue':[0,0,255],
            'blueviolet':[138,43,226],
            'brown':[165,42,42],
            'burlywood':[222,184,135],
            'cadetblue':[95,158,160],
            'chartreuse':[127,255,0],
            'chocolate':[210,105,30],
            'coral':[255,127,80],
            'cornflowerblue':[100,149,237],
            'cornsilk':[255,248,220],
            'crimson':[220,20,60],
            'cyan':[0,255,255],
            'darkblue':[0,0,139],
            'darkcyan':[0,139,139],
            'darkgoldenrod':[184,134,11],
            'darkgray':[169,169,169],
            'darkgreen':[0,100,0],
            'darkgrey':[169,169,169],
            'darkkhaki':[189,183,107],
            'darkmagenta':[139,0,139],
            'darkolivegreen':[85,107,47],
            'darkorange':[255,140,0],
            'darkorchid':[153,50,204],
            'darkred':[139,0,0],
            'darksalmon':[233,150,122],
            'darkseagreen':[143,188,143],
            'darkslateblue':[72,61,139],
            'darkslategray':[47,79,79],
            'darkslategrey':[47,79,79],
            'darkturquoise':[0,206,209],
            'darkviolet':[148,0,211],
            'deeppink':[255,20,147],
            'deepskyblue':[0,191,255],
            'dimgray':[105,105,105],
            'dimgrey':[105,105,105],
            'dodgerblue':[30,144,255],
            'firebrick':[178,34,34],
            'floralwhite':[255,250,240],
            'forestgreen':[34,139,34],
            'fuchsia':[255,0,255],
            'gainsboro':[220,220,220],
            'ghostwhite':[248,248,255],
            'gold':[255,215,0],
            'goldenrod':[218,165,32],
            'gray':[128,128,128],
            'green':[0,128,0],
            'greenyellow':[173,255,47],
            'grey':[128,128,128],
            'honeydew':[240,255,240],
            'hotpink':[255,105,180],
            'indianred':[205,92,92],
            'indigo':[75,0,130],
            'ivory':[255,255,240],
            'khaki':[240,230,140],
            'lavender':[230,230,250],
            'lavenderblush':[255,240,245],
            'lawngreen':[124,252,0],
            'lemonchiffon':[255,250,205],
            'lightblue':[173,216,230],
            'lightcoral':[240,128,128],
            'lightcyan':[224,255,255],
            'lightgoldenrodyellow':[250,250,210],
            'lightgray':[211,211,211],
            'lightgreen':[144,238,144],
            'lightgrey':[211,211,211],
            'lightpink':[255,182,193],
            'lightsalmon':[255,160,122],
            'lightseagreen':[32,178,170],
            'lightskyblue':[135,206,250],
            'lightslategray':[119,136,153],
            'lightslategrey':[119,136,153],
            'lightsteelblue':[176,196,222],
            'lightyellow':[255,255,224],
            'lime':[0,255,0],
            'limegreen':[50,205,50],
            'linen':[250,240,230],
            'magenta':[255,0,255],
            'maroon':[128,0,0],
            'mediumaquamarine':[102,205,170],
            'mediumblue':[0,0,205],
            'mediumorchid':[186,85,211],
            'mediumpurple':[147,112,219],
            'mediumseagreen':[60,179,113],
            'mediumslateblue':[123,104,238],
            'mediumspringgreen':[0,250,154],
            'mediumturquoise':[72,209,204],
            'mediumvioletred':[199,21,133],
            'midnightblue':[25,25,112],
            'mintcream':[245,255,250],
            'mistyrose':[255,228,225],
            'moccasin':[255,228,181],
            'navajowhite':[255,222,173],
            'navy':[0,0,128],
            'oldlace':[253,245,230],
            'olive':[128,128,0],
            'olivedrab':[107,142,35],
            'orange':[255,165,0],
            'orangered':[255,69,0],
            'orchid':[218,112,214],
            'palegoldenrod':[238,232,170],
            'palegreen':[152,251,152],
            'paleturquoise':[175,238,238],
            'palevioletred':[219,112,147],
            'papayawhip':[255,239,213],
            'peachpuff':[255,218,185],
            'peru':[205,133,63],
            'pink':[255,192,203],
            'plum':[221,160,221],
            'powderblue':[176,224,230],
            'purple':[128,0,128],
            'rebeccapurple':[102,51,153],
            'red':[255,0,0],
            'rosybrown':[188,143,143],
            'royalblue':[65,105,225],
            'saddlebrown':[139,69,19],
            'salmon':[250,128,114],
            'sandybrown':[244,164,96],
            'seagreen':[46,139,87],
            'seashell':[255,245,238],
            'sienna':[160,82,45],
            'silver':[192,192,192],
            'skyblue':[135,206,235],
            'slateblue':[106,90,205],
            'slategray':[112,128,144],
            'slategrey':[112,128,144],
            'snow':[255,250,250],
            'springgreen':[0,255,127],
            'steelblue':[70,130,180],
            'tan':[210,180,140],
            'teal':[0,128,128],
            'thistle':[216,191,216],
            'tomato':[255,99,71],
            'turquoise':[64,224,208],
            'violet':[238,130,238],
            'wheat':[245,222,179],
            'white':[255,255,255],
            'whitesmoke':[245,245,245],
            'yellow':[255,255,0],
            'yellowgreen':[154,205,50]
        }

        if old.named_colors_custom_colors is None:
            old['named_colors_custom_colors'] = named_colors
        else:
            old['named_colors_custom_colors'] = named_colors | old['named_colors_custom_colors']

    # Add the comboroles
    comboroles_roles = {}
    for name in old['named_colors_custom_colors']:
        comboroles_roles[name+'_strong'] = [name, 'strong']
        comboroles_roles[name+'_emphasis'] = [name, 'emphasis']
        comboroles_roles[name+'_strong_emphasis'] = [name, 'strong', 'emphasis']
    if 'comboroles_roles' in old:
        old['comboroles_roles'] = old['comboroles_roles'] | comboroles_roles
    else:
        old['comboroles_roles'] = comboroles_roles
    app.config = old

    roles = {k: ColorRole(k) for k, v in old['named_colors_custom_colors'].items()}
    for role in roles:
        app.add_role(role,roles[role])
        app.add_directive(role,ColorAdmonition)
        
    return

class ColorText(nodes.Inline, nodes.TextElement):
    pass

def visit_color_text(self: Writer, node: ColorText):
    self.body.append("<span class=%s>"%(node["style"]))

def depart_color_text(self: Writer, node: ColorText):
    self.body.append("</span>")

class ColorRole(SphinxRole):
    def __init__(self, color_name: str):
        self._color_name = color_name

    def run(self):
        messages = []
        node = ColorText(self.rawtext, self.text)
        node["style"] = f"{self._color_name}"
        return [node], messages
    
class ColorAdmonition(Admonition):

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = Admonition.option_spec
    has_content = True

    def run(self):
        if "class" not in self.options:
            self.options["class"] = [self.name]
        else:
            self.options["class"].append(self.name)
        if len(self.arguments)>0:
            if "no-title" not in self.options["class"]:
                self.arguments[0] = f"{self.arguments[0]}"
            else:
                self.arguments = ["&nbsp;"]
        else:
            if "dropdown" not in self.options["class"] and "show-bar" not in self.options["class"]:
                self.options["class"].append("no-title")
            self.arguments = ["&nbsp;"]
        # Now run the Admonition logic so it behaves the same way
        nodes = super().run()
        return nodes