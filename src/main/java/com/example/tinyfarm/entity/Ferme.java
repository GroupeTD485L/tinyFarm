package com.example.tinyfarm.entity;
import java.time.LocalDateTime;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonManagedReference;

import jakarta.persistence.Entity; // représente une date avec heure sans fuseau horaire
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.persistence.mappedBy;


@Entity
@Table(name = "ferme")
public class Ferme{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // Auto-incrémentation de l'ID
    private Long idFerme;

    @OneToOne(mappedBy = "idFerme") // the value of mappedBy is the name of the association-mapping attribute on the owning side
    private Compte compte; 

    @OneToOne(mappedBy = "proprietaire")
    private Remise remise;

    @OneToOne(mappedBy = "idFerme")
    private Classement classement;

    @OneToMany(mappedBy = "proprietaire")
    private List<Poule> poules;

    @OneToOne(mappedBy = "proprietaire")
    private Vache vache;

    @OneToOne(mappedBy = "proprietaire")
    private Clapier clapier;

    @OneToMany(mappedBy = "idVendeur") //je sais pas du tout comment faire pour qu'il y ait les deux a la fois
    @OneToMany(mappedBy = "idAcheteur")
    private Transaction transaction;

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
        poules = new List<Poule>();
        poules.add(new Poule(idFerme, 'M', null, null, null)); //ajout des poules a la ferme
        poules.add(new Poule(idFerme, 'F', null, null, null));
        poules.add(new Poule(idFerme, 'F', null, null, null));
        remise = new Remise();
        classement = new Classement();
        achatRestant = 12;
    }
}