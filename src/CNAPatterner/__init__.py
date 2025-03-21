# Boilerplate code generated by OVITO Pro 3.12.0
import sys

import numpy
import numpy as np
from ovito.data import *
from ovito.io import *
from ovito.modifiers import *
from ovito.pipeline import *
from ovito.traits import OvitoObject
from ovito.vis import ParticlesVis
from traits.trait_types import *


def row_histogram(a):
    ca = np.ascontiguousarray(a).view([("", a.dtype)] * a.shape[1])
    unique, indices, inverse = np.unique(
        ca, return_index=True, return_inverse=True
    )
    counts = np.bincount(np.reshape(inverse, (inverse.shape[0],)))
    return (a[indices], counts)


predefined_ids = {
    (
        (
            (np.int32(2), np.int32(0), np.int32(0)),
            (np.int32(2), np.int32(1), np.int32(1)),
            (np.int32(3), np.int32(1), np.int32(1)),
            (np.int32(4), np.int32(2), np.int32(1)),
        ),
        (np.int64(1), np.int64(2), np.int64(2), np.int64(1)),
    ): 2,
    (
        (
            (np.int32(4), np.int32(2), np.int32(2)),
            (np.int32(5), np.int32(5), np.int32(5)),
        ),
        (np.int64(10), np.int64(2)),
    ): 3,
    (((np.int32(4), np.int32(2), np.int32(1)),), (np.int64(12),)): 4,
    (((np.int32(5), np.int32(5), np.int32(5)),), (np.int64(12),)): 5,
    (
        (
            (np.int32(1), np.int32(0), np.int32(0)),
            (np.int32(2), np.int32(1), np.int32(1)),
            (np.int32(4), np.int32(2), np.int32(2)),
        ),
        (np.int64(2), np.int64(2), np.int64(2)),
    ): 6,
    (
        (
            (np.int32(2), np.int32(0), np.int32(0)),
            (np.int32(3), np.int32(1), np.int32(1)),
            (np.int32(4), np.int32(2), np.int32(1)),
        ),
        (np.int64(2), np.int64(4), np.int64(1)),
    ): 8,
    (
        (
            (np.int32(2), np.int32(1), np.int32(1)),
            (np.int32(3), np.int32(1), np.int32(1)),
            (np.int32(4), np.int32(2), np.int32(1)),
        ),
        (np.int64(3), np.int64(2), np.int64(2)),
    ): 10,
    (
        (
            (np.int32(2), np.int32(1), np.int32(1)),
            (np.int32(4), np.int32(2), np.int32(1)),
        ),
        (np.int64(4), np.int64(1)),
    ): 11,
    (
        (
            (np.int32(2), np.int32(1), np.int32(1)),
            (np.int32(4), np.int32(2), np.int32(1)),
        ),
        (np.int64(4), np.int64(4)),
    ): 12,
    (
        (
            (np.int32(3), np.int32(1), np.int32(1)),
            (np.int32(3), np.int32(2), np.int32(2)),
            (np.int32(4), np.int32(2), np.int32(2)),
        ),
        (np.int64(4), np.int64(2), np.int64(2)),
    ): 13,
    (
        (
            (np.int32(3), np.int32(2), np.int32(2)),
            (np.int32(5), np.int32(5), np.int32(5)),
        ),
        (np.int64(5), np.int64(1)),
    ): 14,
    (
        (
            (np.int32(3), np.int32(1), np.int32(1)),
            (np.int32(4), np.int32(2), np.int32(1)),
        ),
        (np.int64(6), np.int64(3)),
    ): 15,
    (
        (
            (np.int32(4), np.int32(2), np.int32(1)),
            (np.int32(4), np.int32(2), np.int32(2)),
        ),
        (np.int64(6), np.int64(6)),
    ): 16,
}

edge_idx = [2, 6, 8, 10]
facet_idx = [12, 15]
int_symm_idx = [3, 5, 13, 16]
bulk_idx = [4]
vert_idx = [1, 7, 11, 14]


class ComputeCNAPatterns(ModifierInterface):

    id_feature = Bool(
        True, label="Classify Features", ovito_group="Calculation"
    )

    def modify(self, data, **kwargs):
        try:
            cna_indices = data.particles.bonds["CNA Indices"]
        except TypeError:
            print("You need to compute bond based CNA")
        bond_enumerator = BondsEnumerator(data.particles.bonds)
        seen_cna = predefined_ids.copy()  # Copiamo i valori predefiniti
        counter = (
            max(predefined_ids.values(), default=1) + 1
        )  # Iniziamo con l'ID successivo

        cna_index = data.particles_.create_property(
            "CNAp", dtype=int, components=1
        )
        feature = data.particles_.create_property(
            "Feature Type", dtype=int, components=1
        )
        for particle_index in range(data.particles.count):
            yield (particle_index / data.particles.count)
            bond_index_list = list(
                bond_enumerator.bonds_of_particle(particle_index)
            )
            local_cna_indices = cna_indices[bond_index_list]

            unique_triplets, triplet_counts = row_histogram(local_cna_indices)

            # Converti gli array in tuple immutabili per usarli come chiavi
            key = (tuple(map(tuple, unique_triplets)), tuple(triplet_counts))

            if key not in seen_cna:
                seen_cna[key] = counter
                counter += 1
            cna_index[particle_index] = seen_cna[key]
            if self.id_feature:
                if cna_index[particle_index] in edge_idx:
                    feature[particle_index] = 1
                elif cna_index[particle_index] in facet_idx:
                    feature[particle_index] = 2
                elif cna_index[particle_index] == 4:
                    feature[particle_index] = 3
                elif cna_index[particle_index] in int_symm_idx:
                    feature[particle_index] = 4
                else:
                    feature[particle_index] = 0
