import csv

from collections import defaultdict

from .settings import BASE_DIR, NOW


class PepParsePipeline:

    def __init__(self):
        self.results_dir = BASE_DIR / 'results'
        self.results_dir.mkdir(exist_ok=True)
        self.filename = f'status_summary_{NOW}.csv'

    def open_spider(self, spider):
        self.status_count = defaultdict(int)

    def process_item(self, item, spider):
        self.status_count[item['status']] += 1
        return item

    def close_spider(self, spider):
        with open(self.results_dir / self.filename,
                  mode='w', encoding='utf-8') as f:
            csv.writer(f, dialect=csv.unix_dialect,
                       quoting=csv.QUOTE_NONE).writerows(
                [['Статус', 'Количество'],
                 *(self.status_count.items()),
                 ['Total', sum(self.status_count.values())]
                 ])
