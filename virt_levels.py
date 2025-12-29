def cre_virt_level(sublevel_no,sublevels_quantity, max_sublevels_depth ):
    virt_level = sublevel_no
    #print('type(sublevels_quantity)=>', type(sublevels_quantity))
    #print(max_sublevels_depth)
    num_of_added_zeros = max_sublevels_depth - sublevels_quantity

    for l in range(0, num_of_added_zeros ):
        virt_level = virt_level + '.0'
        #pass
    return virt_level

