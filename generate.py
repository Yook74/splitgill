from subprocess import run

from jinja2 import Environment, FileSystemLoader

template_env = Environment(
    loader=FileSystemLoader('.'),
    block_start_string='#!', block_end_string='!#',
    variable_start_string='#', variable_end_string='#',
    comment_start_string='##', comment_end_string='##'
)
template = template_env.get_template('template.tex')

info = dict(
    donation_date='2022-10-18',
    donor_name='Jim Allen',
    donor_details='cat town'
)

with open('hypha_info.txt') as info_file:
    info['hypha'] = info_file.read().strip()

rendered_str = template.render(**info)

run(
    ['pdflatex', '-jobname', f'{info["donation_date"]} {info["donor_name"]}', '-output-directory', 'generated'],
    input=rendered_str.encode('utf-8'), check=True, capture_output=True
)
