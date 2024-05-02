local lib = LibStub("LibTradeSkillRecipes-1")

if 3 ~= LE_EXPANSION_LEVEL_CURRENT then
	return
end
lib:AddSkillLine(129, "First Aid", 9, {3273,3274,7924,10846,27028,45542,74559})
lib:AddSkillLine(164, "Blacksmithing", 11, {2018,3100,3538,9785,29844,51300,76666})
lib:AddSkillLine(165, "Leatherworking", 11, {2108,3104,3811,10662,32549,51302,81199})
lib:AddSkillLine(171, "Alchemy", 11, {2259,3101,3464,11611,28596,51304,80731})
lib:AddSkillLine(182, "Herbalism", 11, {2366,2368,3570,11993,28695,50300,74519})
lib:AddSkillLine(185, "Cooking", 9, {2550,3102,3413,18260,33359,51296,88053})
lib:AddSkillLine(186, "Mining", 11, {2575,2576,3564,10248,29354,50310,74517})
lib:AddSkillLine(197, "Tailoring", 11, {3908,3909,3910,12180,26790,51309,75156})
lib:AddSkillLine(202, "Engineering", 11, {4036,4037,4038,12656,30350,51306,82774})
lib:AddSkillLine(333, "Enchanting", 11, {7411,7412,7413,13920,28029,51313,74258})
lib:AddSkillLine(356, "Fishing", 9, {7620,7731,7732,18248,33095,51294,88868})
lib:AddSkillLine(393, "Skinning", 11, {8613,8617,8618,10768,32678,50305,74522})
lib:AddSkillLine(755, "Jewelcrafting", 11, {25229,25230,28894,28895,28897,51311,73318})
lib:AddSkillLine(773, "Inscription", 11, {45357,45358,45359,45360,45361,45363,86008})
lib:AddSkillLine(794, "Archaeology", 9, {78670,88961,89718,89719,89720,89721,89722})