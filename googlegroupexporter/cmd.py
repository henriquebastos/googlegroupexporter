from time import sleep

from googlegroupexport.cli import arguments, progressbar, verbosity
from googlegroupexport.exporters import TopicExporter, MailExporter
from googlegroupexport.session import session_factory


def main():
    options = arguments()

    verbosity(options.verbose)

    session = session_factory(
        options.cookies.name, options.workers,
        options.cache_dir, options.cache_forever, options.cache_days
    )

    # Choose exporter class according to selected mode.
    Exporter = dict(csv=TopicExporter, mbox=MailExporter)[options.mode]
    filename = '{}.{}'.format(options.group, options.mode)

    with Exporter(session, filename) as exporter:
        exporter.export(options.group)

        with progressbar() as bar:
            for progress, total in exporter:
                bar.update(progress, total)

                sleep(0.01)

        print(exporter.summary)
