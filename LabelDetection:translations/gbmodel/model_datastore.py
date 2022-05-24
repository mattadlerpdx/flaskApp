
# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .Model import Model
from datetime import datetime
from google.cloud import datastore

def from_datastore(entity):
 """Translates Datastore results into the format expected by the
    application.
    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['label1'],entity['label2'],entity['label3'],entity['label4'],entity['label5'],entity['translated1'],entity['translated2'],entity['translated3'],entity['translated4'],entity['translated5'],entity['image_public_url']]


Class model(Model):
def __init__(self):
        self.client = datastore.Client('cloud-f21-matt-adler-madler')

    def select(self):
        query = self.client.query(kind = 'Pics')
        entities = list(map(from_datastore,query.fetch()))
        return entities
    
    def insert(self,label1,label2,label3,label4,label5,translated1,translated2,translated3,translated4,translated5,image_public_url):
        key = self.client.key('Pics')
        rev = datastore.Entity(key)
        rev.update( {
            'label1': label1,
            'label2' : label2,
            'label3' : label3,
            'label4' : label4,
            'label5' : label5,
            'translated1' : translated1,
            'translated2' : translated2,
            'translated3' : translated3,
            'translated4' : translated4,
            'translated5' : translated5,
            'image_public_url' : image_public_url
            })
        self.client.put(rev)
        return True

    