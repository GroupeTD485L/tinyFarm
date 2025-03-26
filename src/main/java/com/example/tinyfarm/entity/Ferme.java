package com.example.tinyfarm.entity;
import java.time.LocalDateTime;
import java.util.List;
import java.util.ArrayList;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonManagedReference;

import jakarta.persistence.*;
import lombok.Data;


@Entity
@Table(name = "ferme")
@Data 
public class Ferme{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // Auto-incrémentation de l'ID
    private Long idFerme;

    @OneToOne(mappedBy = "idFerme") // the value of mappedBy is the name of the association-mapping attribute on the owning side
    private Compte compte; 

    @OneToOne(mappedBy = "proprietaire")
    private Remise remise;

    @OneToOne(mappedBy = "ferme")
    private Classement classement;

    @OneToMany(mappedBy = "proprietaire")
    private List<Poule> poules;

    @OneToOne(mappedBy = "proprietaire")
    private Vache vache;

    @OneToOne(mappedBy = "proprietaire")
    private Clapier clapier;

    private String nom;
    private int ecus;
    private LocalDateTime enHibernation;
    private int achatRestant;
    private LocalDateTime dernierAchat;

    public Ferme(){}

    public Ferme(String nom){
        this.nom = nom;
        ecus = 1500;
        clapier = new Clapier();
        vache = new Vache();
        poules = new ArrayList<Poule>();
        poules.add(new Poule('M', 2.5, 5)); //ajout des poules a la ferme
        poules.add(new Poule('F', 2.5, 5));
        poules.add(new Poule('F', 2.5, 5));
        remise = new Remise();
        classement = new Classement();
        achatRestant = 12;
    }
}