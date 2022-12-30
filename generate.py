from subprocess import run

from jinja2 import Environment, FileSystemLoader

import google_sheets

template_env = Environment(
    loader=FileSystemLoader('.'),
    block_start_string='#!', block_end_string='!#',
    variable_start_string='#', variable_end_string='#',
    comment_start_string='##', comment_end_string='##'
)
template = template_env.get_template('template.tex')


for donation in google_sheets.get_donations():
    with open('hypha_info.txt') as info_file:
        donation['hypha'] = info_file.read().strip()

    donation['total_value'] = sum([item['value'] for item in donation['donated_items']])

    rendered_str = template.render(**donation)

    run(
        [
            'pdflatex',
            '-jobname', f'{donation["donation_date"].strftime("%Y-%m-%d")} {donation["donor_name"]}',
            '-output-directory', 'generated'
        ],
        input=rendered_str.encode('utf-8'), check=True, capture_output=True
    )
