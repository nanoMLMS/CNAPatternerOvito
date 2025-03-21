# CNAPatterner

CNAPatterner is a custom OVITO modifier that allows for the computation of the CNA Pattern of every atom in the system.

With CNA pattern we mean to which CNA signature, which is a pair property, each atom partecipates to, this property can be used to classify the atom's crystalline structure, for instance an atom in an FCC lattice will partecipate to **12 (4, 2, 1)** signatures, an icosahdrel center to **12 (5, 5, 5)** and so on, as presented in the table below.

To each known patter we assign an integer (also in the table) while patterns not already known are assigned an integer sequentially assigned starting from the highest value from the table.

| **CNAp** | **Description**                                      | **CNAp composition** |
|:--------:|------------------------------------------------------|:--------:|
| 1        | Vertex between two (111) facets and a (100) facet    |[(1, (100)), (2, (211)), (1, (322)), (1, (422))] |
| 2        | Edge between (100) and a slightly distorted (111)    |[(1, (200)), (2, (211)), (2, (311)), (1, (421))] |
| 3        | Atoms lying on a (555) symmetry axis                 |[(10, (422)), (2, (555))] |
| 4        | FCC bulk                                             |[(12, (421))] |
| 5        | Intersection of six five-fold axes                   |[(12, (555))] |
| 6        | Edge between (100) facets                            |[(2, (100)), (2, (211)), (2, (422))] |
| 7        | Vertex on twinning planes shared by (111) facets     |[(2, (200)), (1, (300)), (2, (311)), (1, (322)), (1, (422))] |
| 8        | Edge between (111) re-entrances and (111) facets     |[(2, (200)), (4, (311)), (1, (421))] |
| 9        | Re-entrance delimited by (111) facets                |[(2, (300)), (4, (311)), (2, (421)), (2, (422))] |
| 10       | Edge between (100) and (111) facets                  |[(3, (211)), (2, (311)), (2, (421))] |
| 11       | Vertex shared by (100) and (111) facets              |[(4, (211)), (1, (421))] |
| 12       | (100) facet                                          |[(4, (211)), (4, (421))] |
| 13       | Five-fold symmetry axis (without center)             |[(4, (311)), (2, (322)), (2, (422))] |
| 14       | Five-fold vertex                                     |[(5, (322)), (1, (555))] |
| 15       | (111) face                                           |[(6, (311)), (3, (421))] |
| 16       | Twinning plane                                       |[(6, (421)), (6, (422))] |

## How to use

The computation of the CNA Patterns require the computation of the bond based CNA, the user thus need to either have a structure with bonds or to copmute the bonds using the **Create Bonds** modifier, then they have to apply the **Common Neighbour Analysis** modifier and only then can they apply the **CNAPatterner** modifier.

In the figure below you can see an example with the modifiers applied in the correct order plus a clor coding to color atoms based on the CNAp of the individual particles.

![Screenshot from 2025-03-21 14-56-25](https://github.com/user-attachments/assets/20f3b6df-7598-4f4c-b692-bd30343d0a96)
